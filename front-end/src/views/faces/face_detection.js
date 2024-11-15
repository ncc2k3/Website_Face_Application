import React, { useState } from 'react';
import { Grid, Typography, Box, IconButton, Button } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';
import axios from 'axios';

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
            const response = await axios.post('http://localhost:8800/face_recognition/detect', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            if (response.data.faces && response.data.faces.length > 0) {
                setBoundingBoxes(response.data.faces);
                setNoFaceDetected(false);
            } else {
                setBoundingBoxes([]);
                setNoFaceDetected(true);
            }
        } catch (error) {
            console.error("Error detecting faces:", error);
            setNoFaceDetected(true);
        }
    };

    const handleStartOver = () => {
        setDisplayedImage(null);
        setBoundingBoxes([]);
        setNoFaceDetected(false);
    };

    return (
        <MainCard title="Face Detection Demo">
            <Typography variant="body1" sx={{ fontSize: '1rem', marginBottom: 2, whiteSpace: 'pre-line' }}>
                Face Detection allows you to find faces in an image.{"\n"}
                Along with the position of the faces, Face Detection also provides key points (eyes, nose, mouth) for each face.
            </Typography>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <SubCard>
                        <Typography variant="body2" sx={{ marginBottom: 2 }}>
                            <Typography component="span" sx={{ color: 'red', fontWeight: 'bold', fontSize: "22px" }}>
                                Step 1:
                            </Typography>
                            <br />
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
                                            aspectRatio: '1 / 1',
                                            borderRadius: '8px',
                                            border: '2px solid red',
                                            objectFit: 'cover',
                                            cursor: 'pointer'
                                        }}
                                    />
                                </Grid>
                            ))}
                        </Grid>
                    </SubCard>
                </Grid>

                <Grid item xs={12} sm={6}>
                    <SubCard sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                        <Typography variant="body2" sx={{ marginBottom: 2 }}>
                            <Typography component="span" sx={{ color: 'red', fontWeight: 'bold', fontSize: "22px"}}>
                                Result
                            </Typography>
                        </Typography>
                        <Box
                            sx={{
                                position: 'relative',
                                width: '500px',
                                height: '500px',
                                backgroundColor: displayedImage ? 'transparent' : '#333',
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
                                        <CloudUpload sx={{ fontSize: 250 }} />
                                        <input
                                            hidden
                                            accept="image/*"
                                            type="file"
                                            onChange={handleImageUpload}
                                        />
                                    </IconButton>
                                    <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1, color:"green", fontSize: "18x" }}>
                                        Upload Image or drag and drop in this space<br />
                                        Image should not be beyond 200x200 PX
                                    </Typography>
                                </Box>
                            ) : (
                                <Box sx={{ position: 'relative', width: '100%', height: '100%' }}>
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
                                                borderRadius: '8px'
                                            }}
                                        >
                                            No Face Detected
                                        </Typography>
                                    )}
                                </Box>
                            )}
                        </Box>

                        {displayedImage && (
                            <Button
                                variant="outlined"
                                color="primary"
                                onClick={handleStartOver}
                                sx={{ marginTop: 1, borderRadius: '10px', fontSize: "18px", color: "red" }}
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
