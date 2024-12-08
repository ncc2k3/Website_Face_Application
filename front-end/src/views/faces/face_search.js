import React, { useState } from 'react';
import { Grid, Typography, Box, Button, IconButton } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import axios from 'axios';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

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
    // const [matchResult, setMatchResult] = useState(null); // Trạng thái matched
    // const [confidenceScore, setConfidenceScore] = useState(null); // Điểm độ chính xác
    const [errorMessage, setErrorMessage] = useState(''); // Thông báo lỗi
    const [processing, setProcessing] = useState(false); // Trạng thái đang xử lý

    // Hàm xử lý Face Search API
    const processFaceSearch = async (formData) => {
        setProcessing(true);
        setErrorMessage('');
        try {
            const response = await callApi(API_CONFIG.ENDPOINTS.FACE_SEARCH, formData, true);

            if (response.data.matched) {
                setResultImage(
                    response.data.encoded_images.map((img, index) => ({
                        image: `data:image/jpeg;base64,${img}`,
                        similarity: response.data.similarities[index],
                    }))
                );

                // setMatchResult('Matched');
                // setConfidenceScore((response.data.similarity * 100).toFixed(2)); // Chuyển similarity thành %
            } else {
                setResultImage(null);
                // setMatchResult('No Match Found');
                // setConfidenceScore(null);
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
        // setMatchResult(null);
        // setConfidenceScore(null);
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
                                            objectFit: 'contain', // Giữ ảnh trong khung mà không cắt
                                            overflow: 'hidden', // Ẩn bất kỳ phần nào vượt ra ngoài khung
                                            backgroundColor: '#f8f8f8', // Thêm màu nền để khung đẹp hơn nếu ảnh không lấp đầy
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
                                flexDirection: 'column',
                                alignItems: 'center',
                                gap: '20px',
                                marginBottom: '20px',
                                height: 'auto',
                            }}
                        >
                            {/* Selected Image Section */}
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
                                    backgroundColor: '#f8f8f8',
                                }}
                            >
                                {selectedImage ? (
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
                                ) : (
                                    <IconButton
                                        color="primary"
                                        component="label"
                                        sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}
                                    >
                                        <CloudUpload sx={{ fontSize: 60 }} />
                                        <Typography variant="body2" sx={{ fontSize: '16px', marginTop: '8px' }}>
                                            Upload Image
                                        </Typography>
                                        <input hidden accept="image/*" type="file" onChange={handleImageUpload} />
                                    </IconButton>
                                )}
                            </Box>

                            {/* Result Images Section */}
                            {processing ? (
                                <Typography variant="body1" sx={{ color: '#999', fontSize: '20px', fontStyle: 'italic', textAlign: 'center' }}>
                                    Processing...
                                </Typography>
                            ) : resultImage ? (
                                <Box
                                    sx={{
                                        display: 'flex',
                                        flexDirection: 'column',
                                        alignItems: 'center',
                                        gap: '20px',
                                    }}
                                >
                                    <Typography variant="h6" sx={{ color: '#333', fontWeight: 'bold' }}>
                                        Search Results
                                    </Typography>
                                    <Grid container spacing={2} sx={{ maxHeight: '400px', overflowY: 'auto' }}>
                                        {resultImage.map((result, index) => (
                                            <Grid item xs={6} sm={4} key={index}>
                                                <Box>
                                                    <Box
                                                        component="img"
                                                        src={result.image}
                                                        alt={`Result ${index + 1}`}
                                                        sx={{
                                                            width: '100%',
                                                            height: '150px',
                                                            objectFit: 'contain', // Giữ ảnh trong khung mà không cắt
                                                            overflow: 'hidden', // Ẩn bất kỳ phần nào vượt ra ngoài khung
                                                            backgroundColor: '#f8f8f8', // Thêm màu nền để khung đẹp hơn nếu ảnh không lấp đầy
                                                            borderRadius: '10px',
                                                            border: '3px solid green',
                                                            // transition: 'transform 0.3s',
                                                            // '&:hover': {
                                                            //     transform: 'scale(1.05)',
                                                            // },
                                                        }}
                                                    />
                                                    {/* <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1 }}>
                                                        Similarity: {(result.similarity * 100).toFixed(2)}%
                                                    </Typography> */}
                                                </Box>
                                            </Grid>
                                        ))}
                                    </Grid>
                                </Box>
                            ) : (
                                <Typography
                                    variant="body1"
                                    sx={{ textAlign: 'center', color: 'red', fontWeight: 'bold', marginTop: 2 }}
                                >
                                    {errorMessage || 'No results to display.'}
                                </Typography>
                            )}

                            {/* Reset Button */}
                            {selectedImage && (
                                <Box sx={{ textAlign: 'center', marginTop: 2 }}>
                                    <Button
                                        variant="contained"
                                        color="secondary"
                                        onClick={resetFaceSearch}
                                        sx={{
                                            borderRadius: '8px',
                                            fontWeight: 'bold',
                                            fontSize: '18px',
                                            padding: '8px 16px',
                                            backgroundColor: '#f44336',
                                            '&:hover': {
                                                backgroundColor: '#d32f2f',
                                            },
                                        }}
                                    >
                                        Reset
                                    </Button>
                                </Box>
                            )}
                        </Box>
                    </SubCard>

                </Grid>
            </Grid>
        </MainCard>
    );
};

export default FaceSearch;
