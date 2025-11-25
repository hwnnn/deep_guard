import React from 'react'
import styled, { keyframes } from 'styled-components'
import magnifying_glass from '../assets/magnifying_glass.svg'; 

const float = keyframes`
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-10px) rotate(5deg); }
    100% { transform: translateY(0px) rotate(0deg); }
`;

const StyledAnalyzingPage = () => {
    return (
        <S.AnalyzingPageContainer>
            <S.TitleContainer>
                <S.Title>Analyzing...</S.Title>
            </S.TitleContainer>
            <S.MagnifyingGlass>
                <S.MagnifyingImage src={magnifying_glass} alt="Analyzing Icon"/>
            </S.MagnifyingGlass>
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
        margin-bottom: 50px; 
    `,

    Title: styled.h1`
        font-size: 2.5em; 
        color: #333;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); 
    `,

    SmallMagnifyingIcon: styled.img`
        width: 40px; 
        height: 40px;
        object-fit: contain;
    `,
    
    MagnifyingGlass: styled.div`
        width: 300px;
        height: 300px;
        animation: ${float} 3s ease-in-out infinite; 
        display: flex;
        align-items: center;
        justify-content: center;
        flex-grow: 1; 
    `,
    
    MagnifyingImage: styled.img`
        width: 100%;
        height: 100%;
        object-fit: contain;
    `
}

export default StyledAnalyzingPage