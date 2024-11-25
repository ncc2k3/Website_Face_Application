import React, { useState } from 'react';
import { Grid, Typography, Box, Button, IconButton } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import axios from 'axios';

const sampleImages = [
    { id: 1, src: require('../../assets/images/face/face_search/img14.jpg'), name: 'Angelina Jolie' },
    { id: 2, src: require('../../assets/images/face/face_search/img19.jpg'), name: 'Benedict Cumberbatch' },
    { id: 3, src: require('../../assets/images/face/face_search/img21.jpg'), name: 'Cristiano Ronaldo' },
    { id: 4, src: require('../../assets/images/face/face_search/img27.jpg'), name: 'Gal Gadot' },
    { id: 5, src: require('../../assets/images/face/face_search/img43.jpg'), name: 'Johnny Depp' },
    { id: 6, src: require('../../assets/images/face/face_search/img33.jpg'), name: 'Michelle Yeoh' },
    { id: 7, src: require('../../assets/images/face/face_search/img36.jpg'), name: 'Morgan Freeman' },
    { id: 8, src: require('../../assets/images/face/face_search/img48.jpg'), name: 'Priyanka Chopra Jonas' },
    { id: 9, src: require('../../assets/images/face/face_search/img7.jpg'), name: 'Tom Cruise' },
];

const FaceSearch = () => {
    const [selectedImage, setSelectedImage] = useState(null); // Ảnh được chọn
    const [resultImage, setResultImage] = useState(null); // Ảnh kết quả
    const [matchResult, setMatchResult] = useState(null); // Trạng thái matched
    const [confidenceScore, setConfidenceScore] = useState(null); // Điểm độ chính xác
    const [errorMessage, setErrorMessage] = useState(''); // Thông báo lỗi
    const [processing, setProcessing] = useState(false); // Trạng thái đang xử lý

    // Hàm xử lý Face Search API
    const processFaceSearch = async (formData) => {
        setProcessing(true);
        setErrorMessage('');
        try {
            const response = await axios.post('http://localhost:8800/face_recognition/search', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            if (response.data.matched) {
                setResultImage(`data:image/jpeg;base64,${response.data.image_base64}`); // Hiển thị ảnh từ base64
                setMatchResult('Matched');
                setConfidenceScore((response.data.similarity * 100).toFixed(2)); // Chuyển similarity thành %
            } else {
                setResultImage(null);
                setMatchResult('No Match Found');
                setConfidenceScore(null);
            }
        } catch (error) {
            setErrorMessage('Error processing face search. Please try again.');
        } finally {
            setProcessing(false);
        }
    };

    // Hàm upload ảnh
    const handleImageUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setSelectedImage(imageUrl);

            const formData = new FormData();
            formData.append('image', file);

            await processFaceSearch(formData);
        }
    };

    // Hàm chọn ảnh mẫu
    const handleSampleImageClick = async (imageSrc) => {
        setSelectedImage(imageSrc);

        try {
            const response = await axios.get(imageSrc, { responseType: 'blob' });
            const file = new File([response.data], 'sampleImage.jpg', { type: 'image/jpeg' });

            const formData = new FormData();
            formData.append('image', file);

            await processFaceSearch(formData);
        } catch (error) {
            setErrorMessage('Error processing face search. Please try again.');
        }
    };

    // Hàm reset trạng thái
    const resetFaceSearch = () => {
        setSelectedImage(null);
        setResultImage(null);
        setMatchResult(null);
        setConfidenceScore(null);
        setErrorMessage('');
        setProcessing(false);
    };

    return (
        <MainCard title="Face Search">
            <Grid container spacing={2}>
                {/* Step 1: Select Sample Image */}
                <Grid item xs={12} md={6}>
                    <SubCard title="Step 1: ">
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold', marginBottom: 2 }}>
                            Select a sample image or upload your own
                        </Typography>
                        <Grid container spacing={2}>
                            {sampleImages.map((image) => (
                                <Grid item xs={6} sm={4} key={image.id}>
                                    <Box
                                        component="img"
                                        src={image.src}
                                        alt={image.name}
                                        onClick={() => handleSampleImageClick(image.src)}
                                        sx={{
                                            width: '100%',
                                            height: '150px',
                                            objectFit: 'cover', // Đảm bảo ảnh luôn vừa khung
                                            border: selectedImage === image.src ? '3px solid green' : '2px solid red',
                                            borderRadius: '10px',
                                            cursor: 'pointer',
                                            boxShadow: selectedImage === image.src ? '0 0 10px green' : 'none',
                                        }}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </SubCard>
                </Grid>

                {/* Step 2: Display Results */}
                <Grid item xs={12} md={6}>
                    <SubCard title="Result">
                        <Box
                            sx={{
                                display: 'flex',
                                justifyContent: 'center',
                                alignItems: 'center',
                                gap: '20px',
                                marginBottom: '16px',
                            }}
                        >
                            {/* Selected Image */}
                            <Box
                                component="label"
                                sx={{
                                    position: 'relative',
                                    width: '300px',
                                    height: '300px',
                                    cursor: 'pointer',
                                    borderRadius: '10px',
                                    border: selectedImage ? '3px solid red' : '2px dashed #ccc',
                                    display: 'flex',
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    objectFit: 'cover',
                                }}
                            >
                                {selectedImage && (
                                    <Box
                                        component="img"
                                        src={selectedImage}
                                        alt="Selected"
                                        sx={{
                                            width: '100%',
                                            height: '100%',
                                            objectFit: 'cover',
                                            borderRadius: '10px',
                                        }}
                                    />
                                )}
                                {/* Conditionally show the upload button */}
                                {!selectedImage && (
                                    <IconButton
                                        color="primary"
                                        component="label"
                                        sx={{ marginTop: '16px', backgroundColor: '#f1f1f1', borderRadius: '50%' }}
                                    >
                                        <CloudUpload sx={{ fontSize: 60 }} />
                                        <input hidden accept="image/*" type="file" onChange={handleImageUpload} />
                                    </IconButton>
                                )}
                            </Box>

                            {/* Result Image */}
                            {resultImage && (
                                <Box
                                    component="img"
                                    src={resultImage}
                                    alt="Result"
                                    sx={{
                                        width: '300px',
                                        height: '300px',
                                        objectFit: 'cover',
                                        borderRadius: '10px',
                                        border: '3px solid green',
                                    }}
                                />
                            )}
                        </Box>
                        {/* Matched Result */}
                        {processing ? (
                            <Typography variant="body1" sx={{ color: '#999', fontSize: '20px', fontStyle: 'italic', textAlign: 'center' }}>
                                Processing...
                            </Typography>
                        ) : matchResult ? (
                            <>
                                <Typography
                                    variant="h6"
                                    sx={{ textAlign: 'center', fontWeight: 'bold', fontSize: '22px', color: matchResult === 'Matched' ? 'green' : 'red' }}
                                >
                                    {matchResult}
                                </Typography>
                                <Typography
                                    variant="body1"
                                    sx={{ textAlign: 'center', fontWeight: 'bold', fontSize: '22px', color: '#333' }}
                                >
                                    Score: {confidenceScore}%
                                </Typography>
                            </>
                        ) : (
                            <Typography
                                variant="body1"
                                sx={{ textAlign: 'center', color: 'red', fontWeight: 'bold' }}
                            >
                                {errorMessage}
                            </Typography>
                        )}
                        {/* Reset Button */}
                        {selectedImage && (
                            <Box sx={{ textAlign: 'center', marginTop: 2 }}>
                                <Button
                                    variant="outlined"
                                    color="primary"
                                    onClick={resetFaceSearch}
                                    sx={{ borderRadius: '8px', fontWeight: 'bold', fontSize: '18px' }}
                                >
                                    Reset
                                </Button>
                            </Box>
                        )}
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default FaceSearch;
