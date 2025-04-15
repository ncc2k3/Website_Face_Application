import React, { useState } from 'react';
import { Grid, Typography, Box, IconButton, Button } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import axios from 'axios';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

const sampleImages = [
    { id: 1, src: require('../../assets/images/face/1.jpg'), alt: 'Sample 1' },
    { id: 2, src: require('../../assets/images/face/2.jpg'), alt: 'Sample 2' },
    { id: 3, src: require('../../assets/images/face/3.png'), alt: 'Sample 3' },
    { id: 4, src: require('../../assets/images/face/4.png'), alt: 'Sample 4' }
];

const resizeImage = (file) => {
    return new Promise((resolve) => {
        const img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = () => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = 500;
            canvas.height = 500;
            ctx.drawImage(img, 0, 0, 500, 500);

            canvas.toBlob(resolve, 'image/jpeg', 0.7);
        };
    });
};

const FaceDetection = () => {
    const [displayedImage, setDisplayedImage] = useState(null);
    const [boundingBoxes, setBoundingBoxes] = useState([]);
    const [noFaceDetected, setNoFaceDetected] = useState(false);
    const [faceCount, setFaceCount] = useState(0); // Store number of faces

    const handleImageUpload = async (event) => {
        const file = event.target.files[0];
        if (file) {
            const resizedBlob = await resizeImage(file);
            const imageUrl = URL.createObjectURL(resizedBlob);
            setDisplayedImage(imageUrl);
            detectFaces(resizedBlob);
        }
    };

    const handleSampleImageClick = async (imageSrc) => {
        setDisplayedImage(imageSrc);
        try {
            const response = await axios.get(imageSrc, { responseType: 'blob' });
            const file = new File([response.data], 'sampleImage.jpg', { type: 'image/jpeg' });
            const resizedBlob = await resizeImage(file);
            detectFaces(resizedBlob);
        } catch (error) {
            console.error("Error loading sample image:", error);
        }
    };

    const detectFaces = async (imageBlob) => {
        const formData = new FormData();
        formData.append('image', imageBlob);

        try {
            const response = await callApi(API_CONFIG.ENDPOINTS.FACE_DETECTION, formData, true);

            if (response.data.faces && response.data.confidences) {
                const filteredBoxes = [];
                response.data.faces.forEach((face, index) => {
                    console.log(response.data.confidences[index]);
                    if (response.data.confidences[index] >= 0.85) {
                        filteredBoxes.push(face);
                    }
                });

                if (filteredBoxes.length > 0) {
                    setBoundingBoxes(filteredBoxes);
                    setFaceCount(filteredBoxes.length);
                    setNoFaceDetected(false);
                } else {
                    setBoundingBoxes([]);
                    setFaceCount(0);
                    setNoFaceDetected(true);
                }
            } else {
                setBoundingBoxes([]);
                setNoFaceDetected(true);
                setFaceCount(0);
            }
        } catch (error) {
            console.error("Error detecting faces:", error);
            setBoundingBoxes([]);
            setNoFaceDetected(true);
            setFaceCount(0);
        }
    };

    const handleStartOver = () => {
        setDisplayedImage(null);
        setBoundingBoxes([]);
        setNoFaceDetected(false);
        setFaceCount(0);
    };

    return (
        <MainCard title="Face Detection Demo">
            <Typography variant="body1" sx={{ fontSize: '1rem', marginBottom: 2, whiteSpace: 'pre-line' }}>
                Face Detection allows you to find faces in an image.
            </Typography>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <SubCard title='Step 1'>
                        <Typography variant="body2" sx={{ color: 'red', fontWeight: 'bold', marginBottom: 2 }}>
                            Select from the following sample or upload your own image
                        </Typography>
                        <Grid container spacing={2}>
                            {sampleImages.map((image) => (
                                <Grid item xs={6} key={image.id}>
                                    <Box
                                        component="img"
                                        src={image.src}
                                        alt={image.alt}
                                        onClick={() => handleSampleImageClick(image.src)}
                                        sx={{
                                            width: '100%',
                                            height: 'auto',
                                            aspectRatio: '1 / 1', // Maintain aspect ratio
                                            borderRadius: '8px',
                                            border: '2px solid red',
                                            objectFit: 'contain', // Display within frame without cropping
                                            cursor: 'pointer',
                                            display: 'block', // Ensure image is displayed as block for proper alignment
                                        }}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </SubCard>
                </Grid>

                <Grid item xs={12} sm={6}>
                    <SubCard title='Result'>
                        {faceCount > 0 && (
                            <Typography
                                variant="body2"
                                sx={{
                                    color: 'green',
                                    fontWeight: 'bold',
                                    marginBottom: 1,
                                    fontSize: '18px'
                                }}
                            >
                                Faces Detected: {faceCount}
                            </Typography>
                        )}

                        <Box
                            sx={{
                                position: 'relative',
                                width: '500px',
                                height: '500px',
                                backgroundColor: noFaceDetected ? '#fff' : (displayedImage ? 'transparent' : '#333'),
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                color: '#fff',
                                borderRadius: '10px',
                                overflow: 'hidden',
                                marginBottom: 3,
                                marginTop: 3
                            }}
                        >
                            {!displayedImage ? (
                                <Box display="flex" flexDirection="column" alignItems="center">
                                    <IconButton color="primary" component="label">
                                        <CloudUpload sx={{ fontSize: 150 }} />
                                        <input
                                            hidden
                                            accept="image/*"
                                            type="file"
                                            onChange={handleImageUpload}
                                        />
                                    </IconButton>
                                    <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1, color: 'white', fontSize: '16px' }}>
                                        Upload Image or drag and drop in this space<br />
                                        Image should not be beyond 500x500 px.
                                    </Typography>
                                </Box>
                            ) : (
                                <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
                                    {noFaceDetected && (
                                        <Typography
                                            variant="h6"
                                            sx={{
                                                position: 'absolute',
                                                top: '50%',
                                                left: '50%',
                                                transform: 'translate(-50%, -50%)',
                                                color: 'red',
                                                fontWeight: 'bold',
                                                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                                                padding: '10px',
                                                borderRadius: '8px',
                                                fontSize: '20px'
                                            }}
                                        >
                                            No Face Detected
                                        </Typography>
                                    )}

                                    <Box
                                        component="img"
                                        src={displayedImage}
                                        alt="Displayed"
                                        sx={{
                                            width: '100%',
                                            height: '100%',
                                            objectFit: 'contain'
                                        }}
                                    />

                                    {boundingBoxes.map((box, index) => (
                                        <Box
                                            key={index}
                                            sx={{
                                                position: 'absolute',
                                                border: '2px solid red',
                                                borderRadius: '4px',
                                                top: `${box.y}px`,
                                                left: `${box.x}px`,
                                                width: `${box.width}px`,
                                                height: `${box.height}px`
                                            }}
                                        />
                                    ))}

                                </Box>
                            )}
                        </Box>

                        {displayedImage && (
                            <Button
                                variant="outlined"
                                color="primary"
                                onClick={handleStartOver}
                                sx={{ marginTop: 1, borderRadius: '8px', fontWeight: 'bold', fontSize: '18px' }}
                            >
                                Start Over
                            </Button>
                        )}
                    </SubCard>
                </Grid>
            </Grid>
        </MainCard>
    );
};

export default FaceDetection;