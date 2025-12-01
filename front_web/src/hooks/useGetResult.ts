import { useState } from 'react';
import type { ResultResponse } from '../types/types';

export const useGetResult = () => { 
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [result, setResult] = useState<ResultResponse | null>(null)
    

}