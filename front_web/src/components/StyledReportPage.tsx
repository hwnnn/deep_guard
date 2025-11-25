import React from 'react'
import styled from 'styled-components'

const StyledReportPage = () => {
    return (
        <S.ReportPageContainer>
            <S.TitleContainer>
                <S.Title>신고 절차</S.Title>
            </S.TitleContainer>
            
            <S.ReportBody>
                <S.ReportList>
                    <li>
                        <h3>🚨 1단계. 긴급 피해 발생 시 즉시 신고</h3>
                        <p>
                            영상이 유포 중이거나 협박, 금전 요구, 명예훼손 등 즉각적인 피해가 발생한 경우, **112로 즉시 신고**하세요.
                        </p>
                        <p>
                            가까운 경찰서 사이버수사팀을 직접 방문하거나 사이버범죄 신고시스템 (<S.Link href="https://ecrm.police.go.kr" target="_blank">ecrm.police.go.kr</S.Link>)을 통해 온라인으로도 신고 가능합니다.
                        </p>
                        <p>
                            신고 시에는 영상 URL, 채팅 내용, 캡처 등 **가능한 많은 증거를 확보**해야 합니다.
                        </p>
                    </li>
                    <li>
                        <h3>📞 2단계. 영상 삭제 및 상담 지원 요청</h3>
                        <p>
                            불법 촬영물 또는 딥페이크 영상이 온라인상에 게시된 경우, **디지털성범죄 피해자 지원센터**를 통해 삭제·차단 요청 및 법률·심리 상담 요청이 가능합니다.
                        </p>
                        <p>
                            전문 상담원이 1:1로 지원하며, 피해자 본인뿐 아니라 가족·지인도 상담할 수 있습니다.
                        </p>
                        <S.ContactInfo>
                            <span>전화: 02-735-8994</span>
                            <span>홈페이지: <S.Link href="http://www.digital-sexcrime.kr" target="_blank">www.digital-sexcrime.kr</S.Link></span>
                            <span>운영시간: 평일 09:00~18:00 (주말·공휴일 휴무)</span>
                        </S.ContactInfo>
                    </li>
                </S.ReportList>
            </S.ReportBody>

            <S.ReportBottom>
                <p>정확도가 낮지만 딥페이크로 의심되는 컨텐츠라면,</p>
                <strong>
                    원본 이미지를 다른 각도에서 촬영하거나 해상도가 높은 이미지
                </strong>
                <p>로 교체하여 다시 검사해보세요. 동일 인물의 다양한 사진을 비교하면 정확도가 높아집니다.</p>
            </S.ReportBottom>

        </S.ReportPageContainer>
    )
}

const S = {
    ReportPageContainer : styled.div`
        display: flex;
        flex-direction: column; 
        align-items: center;
        justify-content: flex-start; 
        width: 100vw;
        height: 100vh;
        padding: 20px;
        box-sizing: border-box;
    `,
    
    TitleContainer: styled.div`
        display: flex;
        align-items: center;
        gap: 15px; 
        margin-bottom: 20px; 
    `,

    Title: styled.h1`
        font-size: 2.5em; 
        color: #A9A9A9;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1); 
    `,
    
    ReportBody: styled.div`
        width: 100%;
        flex-grow: 1; /* 남은 공간 차지 */
        text-align: left;
        padding: 0 10px;
    `,

    ReportList: styled.ul`
        list-style: none;
        padding: 0;
        margin: 0;

        li {
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 1px solid #eee;

            h3 {
                color: #dc3545; /* 강조색 */
                margin-top: 0;
                font-size: 1.3em;
            }

            p {
                margin-top: 5px;
                font-size: 1em;
                line-height: 1.5;
            }
        }
    `,

    ContactInfo: styled.div`
        display: flex;
        flex-direction: column;
        margin-top: 10px;
        padding-left: 10px;
        font-size: 0.9em;
        color: #555;
    `,

    Link: styled.a`
        color: #007bff;
        text-decoration: none;
        &:hover {
            text-decoration: underline;
        }
    `,

    ReportBottom: styled.div`
        width: 100%;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;

        p {
            margin: 5px 0;
            line-height: 1.4;
        }

    strong { 
        color: red;

    }
    `,
}


export default StyledReportPage