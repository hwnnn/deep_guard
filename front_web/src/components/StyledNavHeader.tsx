import React from 'react';
import styled from 'styled-components';
import { FaArrowLeft } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

const StyledNavHeader = ({ title = 'DeepFake Detector' }) => {
    const navigate = useNavigate();

    const handleMove = () => {
        navigate('/');
    }

    return (
        <S.AnalHeader>
            <S.HeaderIconWrapper onClick={handleMove}>
                <FaArrowLeft />
            </S.HeaderIconWrapper>
            <S.HeaderTitle>{title}</S.HeaderTitle>
            <S.HeaderSpacer />
        </S.AnalHeader>
    );
}

const S = {
    AnalHeader: styled.nav`
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        width: 100%;
        box-sizing: border-box;
    `,
    HeaderIconWrapper: styled.div`
        cursor: pointer;
        padding: 5px;
        font-size: 1.5em;
    `,
    HeaderTitle: styled.h1`
        font-size: 1.5em;
        margin: 0;
        font-weight: 600;
    `,
    HeaderSpacer: styled.div`
        width: 1.5em; 
        padding: 5px;
    `
};

export default StyledNavHeader;