import React, { useState } from 'react';
import StyledAgreePage from '../components/StyledAgreePage';
import StyledMainPage from '../components/StyledMainPage';

const getCheck = () => {
    const isCheck = localStorage.getItem('isCheck');
    return isCheck === 'true';
}
const MainPage = () => {
    const [isCheck, setIsCheck] = useState(getCheck);

    const handleCheckChange = (newValue:any) => {
        setIsCheck(newValue);
    };

    return (
        isCheck ? 
            <StyledMainPage />
            : 
            <StyledAgreePage onSetCheck={handleCheckChange} /> 
    );
}

export default MainPage;