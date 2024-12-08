import React, { useState } from 'react';
import { Grid, Typography, Box, Button, IconButton } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import axios from 'axios';
import CustomDialog from 'ui-component/CustomDialog';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

const sampleImages = [
    { id: 1, src: require('../../assets/images/face/Angelina-Jolie_fake.png'), alt: 'Sample 1' },
    { id: 2, src: require('../../assets/images/face/Angelina-Jolie_webcam.png'), alt: 'Sample 2' },
    { id: 3, src: require('../../assets/images/face/Angelina-Jolie_real.png'), alt: 'Sample 3' },
    { id: 4, src: require('../../assets/images/face/ronaldo_fake.png'), alt: 'Sample 4' },
    { id: 5, src: require('../../assets/images/face/Cristiano-Ronaldo_webcam.png'), alt: 'Sample 5' },
    { id: 6, src: require('../../assets/images/face/ronaldo_real.png'), alt: 'Sample 6' },
    { id: 7, src: require('../../assets/images/face/Johnny-Depp_fake.png'), alt: 'Sample 7' },
    { id: 8, src: require('../../assets/images/face/Johnny-Depp_webcam.png'), alt: 'Sample 8' },
    { id: 9, src: require('../../assets/images/face/Johnny-Depp_real.png'), alt: 'Sample 9' },
];

const LivenessDetection = () => {
    const [selectedImage, setSelectedImage] = useState(null); // Selected sample or uploaded image
    const [livenessResult, setLivenessResult] = useState(null); // Liveness detection result
    const [errorMessage, setErrorMessage] = useState(''); // Error message
    const [noFaceDetected, setNoFaceDetected] = useState(false); // No face detected flag
    const [dialogOpen, setDialogOpen] = useState(false); // Trạng thái mở form thông báo

    // Hàm xử lý liveness detection
    const processLivenessDetection = async (data) => {
        try {
            const response = await callApi(API_CONFIG.ENDPOINTS.LIVENESS, data, true);

            if (response.data.results && response.data.results.length > 0) {
                const { liveness } = response.data.results[0];
                console.log(response.data.results);
                setLivenessResult(liveness === true ? 'Liveness Passed' : 'Spoofing Detected');
                setNoFaceDetected(false);
                setErrorMessage('');
            } else {
                setNoFaceDetected(true);
                setLivenessResult(null);
                setErrorMessage('');
            }
        } catch (error) {
            setLivenessResult(null);
            setDialogOpen(true);
            setErrorMessage('Error processing liveness detection. Please try again.');
            setNoFaceDetected(false);
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

            await processLivenessDetection(formData);
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

            await processLivenessDetection(formData);
        } catch (error) {
            setLivenessResult(null);
            setErrorMessage('Error processing liveness detection. Please try again.');
            setNoFaceDetected(false);
        }
    };

    // Reset trạng thái
    const resetLiveness = () => {
        setSelectedImage(null);
        setLivenessResult(null);
        setErrorMessage('');
        setDialogOpen(false);
        setNoFaceDetected(false);
    };

    return (
        <MainCard title="Liveness Detection">
            <Grid container spacing={2}>
                {/* Step 1: Sample Image Selection */}
                <Grid item xs={12} md={6}>
                    <SubCard title="Step 1">
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold', marginBottom: 2 }}>
                            Select from the following sample image below or upload your own image to verify liveness.
                        </Typography>
                        <Grid container spacing={2}>
                            {sampleImages.map((image) => (
                                <Grid item xs={6} sm={4} key={image.id}>
                                    <Box
                                        component="img"
                                        src={image.src}
                                        alt={image.alt}
                                        onClick={() => handleSampleImageClick(image.src)}
                                        sx={{
                                            width: '100%',
                                            height: 'auto',
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

                {/* Liveness Result */}
                <Grid item xs={12} md={6}>
                    <SubCard title="Liveness Result">
                        <Box
                            sx={{
                                display: 'flex',
                                flexDirection: 'column',
                                justifyContent: 'center',
                                alignItems: 'center',
                                height: '300px',
                                border: '2px dashed #ccc',
                                borderRadius: '10px',
                                backgroundColor: '#f9f9f9',
                                textAlign: 'center',
                                position: 'relative',
                            }}
                        >
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
                            {selectedImage ? (
                                <>
                                    <Box
                                        component="img"
                                        src={selectedImage}
                                        alt="Selected"
                                        sx={{
                                            width: '150px',
                                            height: '150px',
                                            borderRadius: '50%',
                                            border: '3px solid red',
                                            marginBottom: '16px',
                                        }}
                                    />
                                    {noFaceDetected ? (
                                        <Typography variant="h5" sx={{ color: 'red', fontWeight: 'bold' }}>
                                            No Face Detected
                                        </Typography>
                                    ) : livenessResult ? (
                                        <Typography
                                            variant="h5"
                                            sx={{
                                                fontWeight: 'bold',
                                                color: livenessResult === 'Liveness Passed' ? 'green' : 'red',
                                            }}
                                        >
                                            {livenessResult}
                                        </Typography>
                                    ) : errorMessage ? (
                                        <Typography variant="body1" sx={{ color: 'red', fontWeight: 'bold' }}>
                                            {errorMessage}
                                        </Typography>
                                    ) : (
                                        <Typography variant="body1" sx={{ fontStyle: 'italic', color: '#999' }}>
                                            Processing...
                                        </Typography>
                                    )}
                                </>
                            ) : (
                                <Typography variant="body1" sx={{ fontStyle: 'italic', color: '#999' }}>
                                    Select or upload an image to start liveness detection.
                                </Typography>
                            )}
                        </Box>
                        {selectedImage && (
                            <Button
                                variant="outlined"
                                color="primary"
                                onClick={resetLiveness}
                                sx={{ marginTop: 2, borderRadius: '8px', fontWeight: 'bold', fontSize: '16px' }}
                            >
                                Reset
                            </Button>
                        )}
                    </SubCard>
                </Grid>
            </Grid>
            {/* Custom Dialog */}
            <CustomDialog open={dialogOpen} onClose={resetLiveness} />
        </MainCard>
    );
};

export default LivenessDetection;
