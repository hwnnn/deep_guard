import axios from 'axios';
import type { UploadResponse, ResultResponse} from '../types/types';

export const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 10000,
});


// endpoint : POST /api/inference/upload-file
export const uploadFileForDetection = async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<UploadResponse>('/api/inference/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

    console.log(response.data)
    return response.data;
}

export const getResult = async({task_id}: {task_id: string}): Promise<ResultResponse> => {
    
    const response = await api.get<ResultResponse>(`/api/inference/result/${task_id}`)

    console.log(response.data)
    return response.data;
}