import React, { useRef, useState, type ChangeEvent } from 'react'
import styled from 'styled-components'
import { FaRegCircleQuestion } from "react-icons/fa6";
import { useNavigate } from 'react-router-dom';
import { useDeepfakeDetection } from '../hooks/useDeepfakeDetection';
const getFileUrl = (file: File | null): string | undefined => {
    if (!file) return undefined;
    return URL.createObjectURL(file);
};

const StyledMainPage = () => {

    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState(false);
    const [originFile, setOriginFile] = useState<File|null>(null);
    const [deepfakeFile, setDeepfakeFile] = useState<File|null>(null);
    
    const originalInputRef = useRef<HTMLInputElement>(null);
    const deepfakeInputRef = useRef<HTMLInputElement>(null);

    const handleClick = (value:any) => {
        setIsOpen(!value)
    }

    const handleMove = () => {
        // 파일 업로드 검증 (필수)
        //if (!originFile || !deepfakeFile) {
        //    alert('원본 파일과 딥페이크 파일을 모두 업로드해주세요.');
        //    return;
        if(!deepfakeFile)
          {
            alert('딥 페이크 의심 파일을 업로드 해주세요.')
            return;
          }
        navigate('/analyze', {
          state: {
            targetFile: deepfakeFile
          }
        })
      }

    


    // 2개 일. 때
    //const handleUploadClick = (type: 'original' | 'deepfake') => {
    //    if (type === 'original' && originalInputRef.current){
    //        originalInputRef.current.click();
    //    } else if (type === 'deepfake' && deepfakeInputRef.current){
    //        deepfakeInputRef.current.click();
    //    }
    //}

    const handleUploadClick = () => {
      if (deepfakeInputRef.current)
        deepfakeInputRef.current.click();
    }

    const handleFileChange = (event:ChangeEvent<HTMLInputElement>) => {
            if (event.target.files && event.target.files.length > 0) {
              const file = event.target.files[0];
              const MAX_SIZE = 1048576 * 10;
            if (file.size > MAX_SIZE) {
                alert(`파일 크기가 10MB를 초과합니다. (${(file.size / 1048576).toFixed(2)} MB). 다른 파일을 선택해주세요.`);
                if (event.target) {
                    event.target.value = '';
                }
                return;
            }
            if (deepfakeFile) URL.revokeObjectURL(getFileUrl(deepfakeFile) as string);
              setDeepfakeFile(file);
      }
    }

    //const handleFileChange = (event: ChangeEvent<HTMLInputElement>, type: 'original' | 'deepfake') => {
    //    if (event.target.files && event.target.files.length > 0) {
    //       const file = event.target.files[0];
    //        
    //        const MAX_SIZE = 1048576 * 3;
    //        if (file.size > MAX_SIZE) {
    //            alert(`파일 크기가 3MB를 초과합니다. (${(file.size / 1048576).toFixed(2)} MB). 다른 파일을 선택해주세요.`);
    //            if (event.target) {
    //                event.target.value = '';
     //           }
     //           return;
    //        }

    //        if (type === 'original'){
    //            if (originFile) URL.revokeObjectURL(getFileUrl(originFile) as string);
    //            setOriginFile(file);
    //        } else if (type === 'deepfake'){
    //            if (deepfakeFile) URL.revokeObjectURL(getFileUrl(deepfakeFile) as string);
    //            setDeepfakeFile(file);
    //        }
    //    }
    //}

    const renderPreview = (file: File | null) => {
        if (!file) return null;
        
        const fileUrl = getFileUrl(file);
        const isImage = file.type.startsWith('image/');
        const isVideo = file.type.startsWith('video/');

        if (isImage) {
            return <S.PreviewImage src={fileUrl} alt="Media Preview" />;
        } else if (isVideo) {
            return (
                <S.PreviewVideo controls muted>
                    <source src={fileUrl} type={file.type} />
                    Your browser does not support the video tag.
                </S.PreviewVideo>
            );
        }
        return null;
    }

  return (
    <S.MainContainer>
        <S.MainHeader>
            <S.HeaderSpacer />
            <S.HeaderTitle>DeepFake Detector</S.HeaderTitle>
            <S.HeaderIconWrapper onClick = {() => handleClick(isOpen)}>
                <FaRegCircleQuestion />
            </S.HeaderIconWrapper>
        </S.MainHeader>
        <S.Title>
            Upload Media
        </S.Title>
        <S.SubTitle>
            Detect deepfakes with AI
        </S.SubTitle>

        <S.MainBody>
        {/* <S.LeftImageBox hasFile={!!originFile} onClick={() => handleUploadClick('original')}>
                <input
                    type="file"
                    ref={originalInputRef}
                    onChange={(e) => handleFileChange(e, 'original')}
                    accept="image/*,video/*"
                    style={{ display: 'none' }}
                />
                
                {renderPreview(originFile)}

                {!originFile && (
                    <>
                        <h1>Tab to upload</h1>
                        <p>Upload an Original video or image to check for deepfakes</p>
                        <S.UploadButton>Upload</S.UploadButton>
                    </>
                )}
                {originFile && (
                    <S.FileInfo>
                         <h1>{originFile.name}</h1>
                         <p>File Size: {(originFile.size / 1024 / 1024).toFixed(2)} MB</p>
                         <S.UploadButton onClick={(e) => { e.stopPropagation(); handleUploadClick('original'); }}>Re-upload</S.UploadButton>
                    </S.FileInfo>
                )}
            </S.LeftImageBox>
            <S.RightImageBox hasFile={!!deepfakeFile} onClick={() => handleUploadClick('deepfake')}>
                <input
                    type="file"
                    ref={deepfakeInputRef}
                    onChange={(e) => handleFileChange(e, 'deepfake')}
                    accept="image/*,video/*"
                    style={{ display: 'none' }}
                />
                
                {renderPreview(deepfakeFile)}
                
                {!deepfakeFile && (
                    <>
                        <h1>Tab to upload</h1>
                        <p>Upload a Deepfake video or image to check for deepfakes</p>
                        <S.UploadButton>Upload</S.UploadButton>
                    </>
                )}
                {deepfakeFile && (
                    <S.FileInfo>
                        <h1>{deepfakeFile.name}</h1>
                        <p>File Size: {(deepfakeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        <S.UploadButton onClick={(e) => { e.stopPropagation(); handleUploadClick('deepfake'); }}>Re-upload</S.UploadButton>
                    </S.FileInfo>
                )}
            </S.RightImageBox> */}

            <S.MainImageBox hasFile={!!deepfakeFile} onClick={() => handleUploadClick()}>
                <input
                    type="file"
                    ref={deepfakeInputRef}
                    onChange={(e) => handleFileChange(e)}
                    accept="image/*,video/*"
                    style={{ display: 'none' }}
                />
                
                {renderPreview(deepfakeFile)}
                
                {!deepfakeFile && (
                    <>
                        <h1>Tab to upload</h1>
                        <p>Upload a Deepfake video or image to check for deepfakes</p>
                        <S.UploadButton>Upload</S.UploadButton>
                    </>
                )}
                {deepfakeFile && (
                    <S.FileInfo>
                        <h1>{deepfakeFile.name}</h1>
                        <p>File Size: {(deepfakeFile.size / 1024 / 1024).toFixed(2)} MB</p>
                        <S.UploadButton onClick={(e) => { e.stopPropagation(); handleUploadClick(); }}>Re-upload</S.UploadButton>
                    </S.FileInfo>
                )}

            </S.MainImageBox>
        </S.MainBody>
        <S.CompareButton onClick = {handleMove}>
            Compare Started
        </S.CompareButton>
    </S.MainContainer>
  )
}

const S = {
  MainContainer : styled.div`
    display: flex;
    flex-direction: column; 

    width: 100vw;
    height: calc(100vh - 7vh); 
    padding: 20px;
    box-sizing: border-box;
    text-align: center;
  `,
MainHeader: styled.div`
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

  MainImageBox: styled.div<{hasFile: boolean}>`
    border: 2px dashed ${props => props.hasFile ? 'transparent' : '#ccc'};
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: ${props => props.hasFile ? 'space-between' : 'center'};
    flex-basis: 90%;
    height: 35vh;
    cursor: pointer;
    overflow: hidden;
    position: relative;
    background-color: ${props => props.hasFile ? '#f8f8f8' : 'white'};


    h1 {
      font-size: 1.5em;
      margin-bottom: 10px;
      color: #555;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }

    p {
      font-size: 0.9em;
      color: #777;
      margin-bottom: 20px;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }
  `,
  
  LeftImageBox: styled.div<{hasFile: boolean}>`
    border: 2px dashed ${props => props.hasFile ? 'transparent' : '#ccc'};
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: ${props => props.hasFile ? 'space-between' : 'center'};
    flex-basis: 45%;
    height: 35vh;
    cursor: pointer;
    overflow: hidden;
    position: relative;
    background-color: ${props => props.hasFile ? '#f8f8f8' : 'white'};


    h1 {
      font-size: 1.5em;
      margin-bottom: 10px;
      color: #555;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }

    p {
      font-size: 0.9em;
      color: #777;
      margin-bottom: 20px;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }
  `,

  RightImageBox: styled.div<{hasFile: boolean}>`
    border: 2px dashed ${props => props.hasFile ? 'transparent' : '#ccc'};
    border-radius: 10px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: ${props => props.hasFile ? 'space-between' : 'center'};
    flex-basis: 45%;
    height: 35vh;
    cursor: pointer;
    overflow: hidden;
    position: relative;
    background-color: ${props => props.hasFile ? '#f8f8f8' : 'white'};


    h1 {
      font-size: 1.5em;
      margin-bottom: 10px;
      color: #555;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }

    p {
      font-size: 0.9em;
      color: #777;
      margin-bottom: 20px;
      display: ${props => props.hasFile ? 'none' : 'block'};
    }
  `,
  
  PreviewImage: styled.img`
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 8px;
    flex-grow: 1;
  `,

  PreviewVideo: styled.video`
    width: 100%;
    max-height: 50%;
    object-fit: contain;
    border-radius: 8px;
    flex-grow: 1;
  `,

  FileInfo: styled.div`
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    background: rgba(255, 255, 255, 0.9);
    padding: 10px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    border-top: 1px solid #eee;

    h1 {
        font-size: 1em;
        margin: 0 0 5px 0;
        color: #007bff;
        max-width: 90%;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        display: block;
    }
    p {
        font-size: 0.8em;
        color: #777;
        margin: 0 0 10px 0;
        display: block;
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
    transition: background-color 0.3s;
    &:hover {
      background-color: #0056b3;
    }
  `,

  CompareButton: styled.button`
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
    height: 7vh;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  `
};

export default StyledMainPage