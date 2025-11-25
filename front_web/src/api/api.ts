import axios from 'axios';
import type { DetectionResponse } from '../types/types';

export const api = axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 10000,
});


// endpoint : POST /api/inference/upload-file
export const uploadFileForDetection = async (file: File): Promise<DetectionResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<DetectionResponse>('/api/inference/upload-file', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });

    return response.data;
}