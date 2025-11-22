import React from 'react';
import styled from 'styled-components';

type StyledAgreePageProps = {
  onSetCheck: (value: boolean) => void; 
}

const StyledAgreePage = ({onSetCheck}:StyledAgreePageProps) => {

  const handleClick = () => {
    onSetCheck(true);
    localStorage.setItem('isCheck', 'true');
  }

  return (
    <>
    <S.AgreePageContainer>
      <S.Title>DeepFake Detector</S.Title> 
      <S.SubTitle>Detect deepfakes with AI</S.SubTitle> 
      <S.Description> 
        Our app uses advanced computer vision and deep learning techniques to analyze videos and images, identifying subtle inconsistencies that indicate manipulation.
      </S.Description>
    </S.AgreePageContainer>
    <S.StartButton onClick={handleClick}>
        Get Started
    </S.StartButton>
    </>
  )
}

const S = {
  AgreePageContainer : styled.div`
    display: flex;
    flex-direction: column; 

    width: 100vw;
    height: calc(100vh - 7vh); 
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
    font-size: 1.5em;
    margin-bottom: 1.5em;
  `,
  Description: styled.p`
    font-size: 1.1em;
    color: #666;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto;
  `,
  StartButton: styled.button`
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 100px;
    padding: 15px 30px;
    font-size: 1.5em;
    cursor: pointer;
    transition: background-color 0.3s;

    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 7h;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  `
};

export default StyledAgreePage;