import React, { useEffect, useState } from 'react'
import styled from 'styled-components';
import StyledAnalyzingPage from '../components/StyledAnalyzingPage';
import StyledResultPage from '../components/StyledAnalResultPage';
import { useLocation, useNavigate } from 'react-router-dom';
import { FaArrowLeft } from "react-icons/fa";
import { useDeepfakeDetection } from '../hooks/useDeepfakeDetection';
const AnalyzePage = () => {

    const navigate = useNavigate();
    const location = useLocation();
    const {detectDeepfake, isLoading, error, result} = useDeepfakeDetection();
    const file = location.state?.targetFile;

    useEffect(() => {
      detectDeepfake(file);
    },[])

    const handleMove = () => {

    }

    const handleRetry = () => {
        if (file) {
            console.log("재시도 요청됨");
            detectDeepfake(file); // 훅 재호출
        }
    };

  return (
    <S.AnalyzePageContainer>
        {/* <S.AnalHeader>
        <S.HeaderIconWrapper onClick = {handleMove}>
            <FaArrowLeft />
        </S.HeaderIconWrapper>
        <S.HeaderTitle>DeepFake Detector</S.HeaderTitle>
        <S.HeaderSpacer />
        </S.AnalHeader> */}
        <S.MainBody>
            {isLoading ? <StyledAnalyzingPage/> : <StyledResultPage error = {error} result = {result} onRetry={handleRetry} />}
        </S.MainBody> 
    </S.AnalyzePageContainer>
  )
}

const S = {
    AnalyzePageContainer : styled.div`
    display: flex;
    flex-direction: column; 
    width: 100vw;
    height: calc(100vh - 7vh); 
    padding: 20px;
    box-sizing: border-box;
    text-align: center;
  `,
    AnalHeader: styled.div`
    display: flex; 
    justify-content: space-between; 
    align-items: center; 
    width: 100%; 
    padding: 10px 0; 
    
    font-size: 1.5em;
    font-weight: bold; 
    color: #333; 
  `,

  HeaderTitle: styled.span`
  `,
  
  HeaderIconWrapper: styled.div`
    cursor: pointer;
  `,
  HeaderSpacer: styled.div`
    width: 24px; 
    height: 24px;
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
    flex-grow: 1;
    margin-bottom: 20px;
  `,

}

export default AnalyzePage