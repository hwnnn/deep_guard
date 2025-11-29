import { useLocation, useNavigate } from 'react-router-dom';
import styled from 'styled-components';
import type { ResultResponse } from '../types/types';
const StyledResultPage = () => {

    const location = useLocation();
    const navigate = useNavigate();

    const state = location.state as { resultData: ResultResponse} | null;
    const result = state?.resultData;


    const orig_image64 = `data:image/jpeg;base64,${result?.detection_result.orin_img}`
    const result_image64 = `data:image/jpeg;base64,${result?.detection_result.result_img}`

    return (
        <S.MainContainer>
            <S.Title>DeepFake</S.Title>
            <S.SubTitle>
                <p>{result?.detection_result.is_fake ? "딥페이크가 맞습니다" : "딥페이크가 아닙니다"}</p>
                <p>Confidence: {result ? result?.detection_result.confidence : '-' }</p>
                <p>판정 : {result?.detection_result.verdict}</p>

            </S.SubTitle>

            <S.MainBody>
                <S.MainImageBox>
                    <S.PreviewImage src={orig_image64} alt="Orin_Img"/>
                    <S.PreviewImage src={result_image64} alt="Result_img"/>
                </S.MainImageBox>
            </S.MainBody>

            <S.ResultSection>
                <h2>결과 분석</h2>

                {result ? (
                    <>
                    </>
                ) : (
                    <p>데이터 없음</p>
                )}
            </S.ResultSection>

        </S.MainContainer>
    );
};

const S = {
    MainContainer: styled.div`
        display: flex;
        flex-direction: column;
        width: 100vw;
        padding: 20px;
        box-sizing: border-box;
        text-align: center;
    `,

    Title: styled.h1`
        font-size: 2em;
        color: #333;
        margin-bottom: 0.5em;
    `,

    SubTitle: styled.h2`
        font-size: 1em;
        margin-bottom: 1.5em;
    `,

    MainBody: styled.div`
        display: flex;
        justify-content: space-around;
        align-items: flex-start;
        gap: 20px;
        margin-bottom: 30px;
    `,

    MainImageBox: styled.div`
        border: 2px dashed #ccc;
        border-radius: 10px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-basis: 70%;
        height: 35vh;
        cursor: pointer;
        overflow: hidden;
        position: relative;
        background-color: white;
    
    
        h1 {
          font-size: 1.5em;
          margin-bottom: 10px;
          color: #555;
          display: 'none';
        }
    
        p {
          font-size: 0.9em;
          color: #777;
          margin-bottom: 20px;
          display: 'none';
        }
      `,

    LeftImageBox: styled.div<{ hasFile: boolean }>`
        border: 2px dashed ${props => props.hasFile ? 'transparent' : '#ccc'};
        border-radius: 10px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: ${props => props.hasFile ? 'space-between' : 'center'};
        flex-basis: 45%;
        height: 35vh;
        cursor: default;
        overflow: hidden;
        position: relative;
        background-color: ${props => props.hasFile ? '#f8f8f8' : 'white'};
    `,

    RightImageBox: styled.div<{ hasFile: boolean }>`
        border: 2px dashed ${props => props.hasFile ? 'transparent' : '#ccc'};
        border-radius: 10px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: ${props => props.hasFile ? 'space-between' : 'center'};
        flex-basis: 45%;
        height: 35vh;
        cursor: default;
        overflow: hidden;
        position: relative;
        background-color: ${props => props.hasFile ? '#f8f8f8' : 'white'};
    `,

    PreviewImage: styled.img`
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 8px;
    `,

    PreviewVideo: styled.video`
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 8px;
    `,

    FileInfo: styled.div`
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.9);
        padding: 10px;
        box-sizing: border-box;
        text-align: center;
        border-top: 1px solid #eee;

        h1 {
            font-size: 1em;
            margin: 0 0 5px 0;
            color: #007bff;
        }

        p {
            font-size: 0.8em;
            margin: 0 0 10px 0;
            color: #777;
        }
    `,

    UploadButton: styled.button`
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 15px;
        font-size: 0.9em;
        cursor: pointer;
        transition: 0.3s;

        &:hover {
            background-color: #0056b3;
        }
    `,

    ResultSection: styled.div`
        width: 100%;
        padding: 20px;
        text-align: left;
        border-top: 1px solid #eee;
        margin-top: 20px;

        h2 {
            margin-bottom: 10px;
            color: #333;
        }

        p {
            margin: 5px 0;
            color: #555;
        }
    `,
};

export default StyledResultPage;