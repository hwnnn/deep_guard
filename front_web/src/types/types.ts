export type DetectionResponse = {
    success: boolean;
    filename: string;
    detection_result: {
        is_fake: boolean;
        confidence: number;
        verdict: string;
        fake_probability: number;
        real_probability: number;
    };
}

export type UploadResponse = {
    task_id: string,
    status: string,
    message: string
}

export type ResultResponse = {
    task_id: string;
    filename: string;
    file_size: number;
    timestamp: string;
    detection_result: {
        is_fake: boolean;
        confidence: number;
        fake_probability: number;
        real_probability: number;
        verdict: string;
    };
    analysis: {
        ensemble_method: string;
        models_used: number;
        fake_votes: number;
        model_results: {
            [modelName: string]: {
                fake_probability: number;
                confidence: number;
            };
        };
    };
    model_info: {
        name: string;
    };
};