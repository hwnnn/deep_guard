import React, { useState } from 'react'
import styled from 'styled-components';
import successImg from '../assets/success.svg';
import failImg from '../assets/fail.svg';
import { useNavigate } from 'react-router-dom';
import type { DetectionResponse } from '../types/types';

type AnalResultPageProps = {
    error: string | null;
    result: DetectionResponse | null;
    onRetry: () => void;
}

const AnalResultPage = ({error, result, onRetry} : AnalResultPageProps) => {
    

    const navigate = useNavigate();

    const isError = !!error;

    const ResultText = isError ? 'Analyze Failed' : 'Analyze Success';
    const ResultImg = isError ? failImg : successImg;

    const handleClick = () => {
        if (isError)
        {
            //navigate('/');
            onRetry();
            console.error(error);
        } else {
            navigate('/result', { 
                state: { 
                    resultData: result // 도착한 페이지에서 location.state.resultData로 사용
                } 
            });
        }

    }

    if (!result && !error) {
            return <div>데이터가 없습니다.</div>;
        }


    return (
        <S.AnalyzingPageContainer>
            <S.TitleContainer>
                <S.Title $isError={isError}>{ResultText}</S.Title>
            </S.TitleContainer>
            <S.ResultBody>
                <S.ResultImg src={ResultImg} alt={ResultText}/>
            </S.ResultBody>

            <S.ResultButton onClick = {handleClick}>
                {error ? 'Retry' : 'Show Report'}
            </S.ResultButton>
        </S.AnalyzingPageContainer>
    )
}

const S = {
    AnalyzingPageContainer : styled.div`
        display: flex;
        flex-direction: column; 
        align-items: center;
        justify-content: flex-start; 
        width: 100%;
        height: 100%;
        min-height: 50vh; 
        padding: 40px;
        box-sizing: border-box;
    `,
    
    TitleContainer: styled.div`
        display: flex;
        align-items: center;
        gap: 15px; 
    `,

    Title: styled.h1<{ $isError: boolean }>`
        font-size: 4em; 
        color: ${props => (props.$isError ? '#dc3545' : '#333')};
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); 
    `,

    SmallMagnifyingIcon: styled.img`
        width: 40px; 
        height: 40px;
        object-fit: contain;
    `,
    
    ResultBody: styled.div`
        width: 200px;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-grow: 1; 
    `,
    
    ResultImg: styled.img`
        width: 100%;
        height: 100%;
        object-fit: contain;
    `,

    ResultButton: styled.button`
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 100px;
    padding: 15px 30px;
    font-size: 1.5em;
    cursor: pointer;
    transition: background-color 0.3s;

    width: 100%;
    height: 7vh;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    `
}

export default AnalResultPage