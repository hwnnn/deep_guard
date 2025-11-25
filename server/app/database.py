"""
Database module for Redis (cache) and MongoDB (persistent storage)
"""
import redis
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from typing import Optional
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD") or None  # Empty string → None
REDIS_TTL = int(os.getenv("REDIS_TTL", "86400"))

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "deep_guard")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "inference_results")

# Log configuration on import (for debugging)
if os.getenv("DEBUG", "false").lower() == "true":
    print(f"[Database Config] Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
    print(f"[Database Config] MongoDB: {MONGODB_URL} -> {MONGODB_DB}.{MONGODB_COLLECTION}")
    print(f"[Database Config] Redis TTL: {REDIS_TTL}s ({REDIS_TTL//3600}h)")


class DatabaseManager:
    """Hybrid storage: Redis for cache, MongoDB for persistence"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.mongo_client: Optional[AsyncIOMotorClient] = None
        self.mongo_collection = None
        self._in_memory_fallback: dict = {}
    
    def connect_redis(self):
        """Connect to Redis for caching"""
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD if REDIS_PASSWORD else None,
                decode_responses=True
            )
            self.redis_client.ping()
            print(f"✅ Redis connected: {REDIS_HOST}:{REDIS_PORT}")
        except Exception as e:
            print(f"⚠️  Redis unavailable: {e}")
            print("   → Fallback: in-memory cache")
            self.redis_client = None
    
    def connect_mongodb(self):
        """Connect to MongoDB for persistent storage"""
        try:
            self.mongo_client = AsyncIOMotorClient(MONGODB_URL)
            self.mongo_collection = self.mongo_client[MONGODB_DB][MONGODB_COLLECTION]
            # Test sync connection
            sync_client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
            sync_client.server_info()
            sync_client.close()
            print(f"✅ MongoDB connected: {MONGODB_URL}")
        except Exception as e:
            print(f"⚠️  MongoDB unavailable: {e}")
            print("   → Fallback: in-memory storage only")
            self.mongo_client = None
            self.mongo_collection = None
    
    def disconnect(self):
        """Close all connections"""
        if self.redis_client:
            self.redis_client.close()
        if self.mongo_client:
            self.mongo_client.close()
    
    async def save(self, task_id: str, data: dict):
        """Save to Redis (cache) + MongoDB (persistent)"""
        saved = False
        
        # Redis: Fast cache with TTL
        if self.redis_client:
            try:
                self.redis_client.setex(
                    f"task:{task_id}",
                    REDIS_TTL,
                    json.dumps(data, ensure_ascii=False)
                )
                saved = True
            except Exception as e:
                print(f"Redis save error: {e}")
        
        # MongoDB: Persistent storage
        if self.mongo_collection is not None:
            try:
                doc = data.copy()
                doc["_id"] = task_id
                await self.mongo_collection.insert_one(doc)
                saved = True
            except Exception as e:
                print(f"MongoDB save error: {e}")
        
        # Fallback: In-memory
        if not saved:
            self._in_memory_fallback[task_id] = data
    
    async def get(self, task_id: str) -> Optional[dict]:
        """Get from Redis → MongoDB → Fallback"""
        
        # 1. Try Redis (cache)
        if self.redis_client:
            try:
                cached = self.redis_client.get(f"task:{task_id}")
                if cached and isinstance(cached, str):
                    return json.loads(cached)
            except Exception as e:
                print(f"Redis get error: {e}")
        
        # 2. Try MongoDB (persistent)
        if self.mongo_collection is not None:
            try:
                doc = await self.mongo_collection.find_one({"_id": task_id})
                if doc:
                    doc.pop("_id", None)
                    # Re-cache to Redis
                    if self.redis_client:
                        try:
                            self.redis_client.setex(
                                f"task:{task_id}",
                                REDIS_TTL,
                                json.dumps(doc, ensure_ascii=False)
                            )
                        except:
                            pass
                    return doc
            except Exception as e:
                print(f"MongoDB get error: {e}")
        
        # 3. Fallback
        return self._in_memory_fallback.get(task_id)
    
    async def stats(self) -> Optional[dict]:
        """Get statistics from MongoDB"""
        if self.mongo_collection is None:
            return None
        
        try:
            total = await self.mongo_collection.count_documents({})
            fake = await self.mongo_collection.count_documents({"detection_result.is_fake": True})
            return {
                "total": total,
                "fake": fake,
                "real": total - fake,
                "fake_rate": fake / total if total > 0 else 0
            }
        except:
            return None


# Global instance
db = DatabaseManager()


def get_db() -> DatabaseManager:
    """Dependency for FastAPI"""
    return db
