import React, { useState } from 'react';
import { Grid, Typography, Box, IconButton, Button } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

import CustomDialog from 'ui-component/CustomDialog';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

const FaceComparison = () => {
    const [firstImage, setFirstImage] = useState(null); // Original display image
    const [resizedFirstFile, setResizedFirstFile] = useState(null); // Resized image
    const [secondImage, setSecondImage] = useState(null); // Original display image
    const [resizedSecondFile, setResizedSecondFile] = useState(null); // Resized image
    const [comparisonResult, setComparisonResult] = useState(null);
    const [error, setError] = useState(null);
    const [dialogOpen, setDialogOpen] = useState(false); // Form notification state

    // Resize image to 224x224 pixels
    const resizeImage = (file) => {
        return new Promise((resolve) => {
            const img = new Image();
            img.src = URL.createObjectURL(file);
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = 224;
                canvas.height = 224;
                ctx.drawImage(img, 0, 0, 224, 224);
                canvas.toBlob(resolve, 'image/jpeg', 0.7);
            };
        });
    };

    // Handle first image upload
    const handleFirstImageUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file); // Original image for display
            setFirstImage(imageUrl);

            const resizedBlob = await resizeImage(file); // Resize image for sending
            setResizedFirstFile(resizedBlob);
        }
    };

    // Handle second image upload
    const handleSecondImageUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file); // Original image for display
            setSecondImage(imageUrl);

            const resizedBlob = await resizeImage(file); // Resize image for sending
            setResizedSecondFile(resizedBlob);
        }
    };

    // Call API for face comparison
    const compareFaces = async () => {
        if (!resizedFirstFile || !resizedSecondFile) {
            setError("Both images are required for comparison");
            return;
        }

        const formData = new FormData();
        formData.append("image1", resizedFirstFile);
        formData.append("image2", resizedSecondFile);

        try {
            const response = await callApi(API_CONFIG.ENDPOINTS.FACE_COMPARISON, formData, true);

            // console.log(response.data[0]?.error);
            // Kiểm tra nếu response.data là một mảng và chứa lỗi
            if (Array.isArray(response.data) && response.data[0]?.error) {
                setError(response.data[0].error); // Record error from back-end
                setDialogOpen(true); // Open error dialog
                return;
            }

            const { verified, distance, threshold } = response.data;
            console.log(verified, distance, threshold);
            const score = ((1 - distance) * 100).toFixed(2); // Convert to percentage
            console.log(score);
            setComparisonResult({
                matched: verified,
                score: `${score}%`,
            });
            // if (score >= 60) {
            //     setComparisonResult({
            //         matched: verified,
            //         score: `${score}%`,
            //     });
            // } else {
            //     setComparisonResult({
            //         matched: false,
            //         score: `${score}%`,
            //     });
            // }
            setError(null);
        } catch (err) {
            setComparisonResult(null);
            setError("An error occurred during comparison. Please try again.");
            setDialogOpen(true);
        }
        setDialogOpen(false); // Close notification form if open
    };


    // Reset images and result
    const reset = () => {
        setFirstImage(null);
        setSecondImage(null);
        setResizedFirstFile(null);
        setResizedSecondFile(null);
        setComparisonResult(null);
        setError(null);
        setDialogOpen(false); // Đóng form thông báo nếu mở
    };

    return (
        <MainCard title="Face Comparison Demo">
            <Typography variant="body1" sx={{ fontSize: '1rem', marginBottom: 2 }}>
                Face Comparison allows you to tell if two facial images belong to the same person. The images will be resized to 224x224 pixels for processing.
            </Typography>
            <Grid container spacing={2}>
                {/* Step 1 - First Image Upload */}
                <Grid item xs={12} sm={4}>
                    <SubCard title="Step 1">
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold' }}>
                            Upload an image
                        </Typography>
                        <Box
                            sx={{
                                width: '100%',
                                height: '300px',
                                backgroundColor: firstImage ? 'transparent' : '#333',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexDirection: 'column',
                                color: '#fff',
                                borderRadius: '10px',
                                border: '2px solid red',
                                overflow: 'hidden',
                                marginTop: 2,
                            }}
                        >
                            {!firstImage ? (
                                <IconButton color="primary" component="label">
                                    <CloudUpload sx={{ fontSize: 90 }} />
                                    <input
                                        hidden
                                        accept="image/*"
                                        type="file"
                                        onChange={handleFirstImageUpload}
                                    />
                                </IconButton>
                            ) : (
                                <Box
                                    component="img"
                                    src={firstImage}
                                    alt="First Image"
                                    sx={{
                                        width: '100%',
                                        height: '100%',
                                        objectFit: 'contain', // Hiển thị ảnh gốc vừa khung
                                    }}
                                />
                            )}
                        </Box>
                    </SubCard>
                </Grid>

                {/* Step 2 - Second Image Upload */}
                <Grid item xs={12} sm={4}>
                    <SubCard title="Step 2">
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold' }}>
                            Upload another image
                        </Typography>
                        <Box
                            sx={{
                                width: '100%',
                                height: '300px',
                                backgroundColor: secondImage ? 'transparent' : '#333',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexDirection: 'column',
                                color: '#fff',
                                borderRadius: '10px',
                                border: '2px solid red',
                                overflow: 'hidden',
                                marginTop: 2,
                            }}
                        >
                            {!secondImage ? (
                                <IconButton color="primary" component="label">
                                    <CloudUpload sx={{ fontSize: 90 }} />
                                    <input
                                        hidden
                                        accept="image/*"
                                        type="file"
                                        onChange={handleSecondImageUpload}
                                    />
                                </IconButton>
                            ) : (
                                <Box
                                    component="img"
                                    src={secondImage}
                                    alt="Second Image"
                                    sx={{
                                        width: '100%',
                                        height: '100%',
                                        objectFit: 'contain', // Hiển thị ảnh gốc vừa khung
                                    }}
                                />
                            )}
                        </Box>
                    </SubCard>
                </Grid>

                {/* Result - Comparison Result */}
                <Grid item xs={12} sm={4}>
                    <SubCard title="Result">
                        {/* <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold' }}>
                            Score of 60% or more is a match
                        </Typography> */}
                        <Box
                            sx={{
                                width: '100%',
                                height: '300px',
                                backgroundColor: '#333',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexDirection: 'column',
                                color: '#fff',
                                borderRadius: '10px',
                                border: '2px solid red',
                                overflow: 'hidden',
                                marginTop: 2,
                            }}
                        >
                            {comparisonResult ? (
                                <Typography variant="h2" sx={{ color: comparisonResult.matched ? 'white ' : 'red' }}>
                                    {comparisonResult.matched
                                        ? `Matched!`
                                        : `Not Matched!`}
                                </Typography>
                            ) : error ? (
                                <Typography variant="h6" sx={{ color: 'red' }}>
                                    {error}
                                </Typography>
                            ) : (
                                <Typography variant="h2" sx={{ color: '#fff', fontSize: '30px' }}>
                                    ...
                                </Typography>
                            )}
                        </Box>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={compareFaces}
                            sx={{ marginTop: 2 }}
                        >
                            Compare
                        </Button>
                        <Button
                            variant="outlined"
                            color="secondary"
                            onClick={reset}
                            sx={{ marginTop: 2, marginLeft: 2 }}
                        >
                            Reset
                        </Button>
                    </SubCard>
                </Grid>
            </Grid>

            {/* Custom Dialog */}
            <CustomDialog open={dialogOpen} onClose={reset} />

        </MainCard>
    );
};

export default FaceComparison;