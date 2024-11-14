import React, { useState } from 'react';
import { Grid, Typography, Box, IconButton } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

const FaceComparison = () => {
    const [firstImage, setFirstImage] = useState(null);
    const [secondImage, setSecondImage] = useState(null);

    // Hàm xử lý khi tải ảnh lên
    const handleFirstImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setFirstImage(imageUrl);
        }
    };

    const handleSecondImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setSecondImage(imageUrl);
        }
    };

    return (
        <MainCard title="Face Comparison Demo">
            <Typography variant="body1" sx={{ fontSize: '1rem', marginBottom: 2 }}>
                Face Comparison allows you to tell if two facial images belong to the same person. Unlike Face Search which needs the registration and subsequent storage of face images on our server, Face Comparison works only on the face images provided without storing any data on our server.
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
                                    <CloudUpload sx={{ fontSize: 60 }} />
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
                                        objectFit: 'cover',
                                    }}
                                />
                            )}
                            {!firstImage && (
                                <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1 }}>
                                    Upload Image or drag and drop in this space
                                </Typography>
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
                                    <CloudUpload sx={{ fontSize: 60 }} />
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
                                        objectFit: 'cover',
                                    }}
                                />
                            )}
                            {!secondImage && (
                                <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1 }}>
                                    Upload Image or drag and drop in this space
                                </Typography>
                            )}
                        </Box>
                    </SubCard>
                </Grid>

                {/* Result - Comparison Result */}
                <Grid item xs={12} sm={4}>
                    <SubCard title="Result">
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold' }}>
                            Score of 66% or more is a match
                        </Typography>
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
                            <Typography variant="h6" sx={{ color: '#fff' }}>
                                ...
                            </Typography>
                        </Box>
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default FaceComparison;
