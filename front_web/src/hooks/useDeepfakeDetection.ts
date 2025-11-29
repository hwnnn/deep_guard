import { useState } from 'react';
import { getResult, uploadFileForDetection } from '../api/api';
import type { ResultResponse, UploadResponse} from '../types/types';
import { data } from 'react-router-dom';

export const useDeepfakeDetection = () => {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ResultResponse | null>(null);
    
    const detectDeepfake = async (file: File) => {
        setIsLoading(true);
        setError(null);
        setResult(null);

        try {
            const uploadResponse = await uploadFileForDetection(file);
            if (uploadResponse && uploadResponse.task_id) {
                
                const finalResult = await getResult({ task_id: uploadResponse.task_id });
                
                setResult(finalResult);
            } else {
                throw new Error("파일 업로드에 실패했거나 Task ID를 받지 못했습니다.");
            }

        } catch (err: any) {
            const errorMessage = err.response?.data?.detail || '딥페이크 탐지 중 오류가 발생했습니다.';
            setError(errorMessage);
            console.error("Detection Error:", err);
        } finally {
            setIsLoading(false);
        }
    }

    return {
        detectDeepfake,
        isLoading,
        error,
        result
    };
}