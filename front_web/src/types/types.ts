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