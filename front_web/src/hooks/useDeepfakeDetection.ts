import { useState } from 'react';
import { uploadFileForDetection } from '../api/api';
import type { DetectionResponse } from '../types/types';

export const useDeepfakeDetection = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<DetectionResponse | null>(null)
    
    const detectDeepfake = async (file: File) => {
        setIsLoading(true);
        //setError(null);
        //setResult(null)

        try{
            const data = await uploadFileForDetection(file);
            setResult(data);
            console.log("판정 결과: ", data.detection_result.verdict);
        } catch (error: any){
            setError(error.response?.data?.detail || '딥 페이크 탐지 중 오류 발생')
            console.error(error)
        } finally{
            setIsLoading(false)
        }
    }

    return {
        detectDeepfake, // 이것만 꺼내 사용
        isLoading,
        error,
        result
    }

}
