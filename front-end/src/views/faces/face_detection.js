import React, { useState } from 'react';
import { Grid, Typography, Box, IconButton, Button } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

// project imports
import MainCard from 'ui-component/cards/MainCard';
import SubCard from 'ui-component/cards/SubCard';

const sampleImages = [
    { id: 1, src: 'https://freepngdownload.com/image/thumb/face-free-png-image.png', alt: 'Sample 1' },
    { id: 2, src: 'https://img.freepik.com/free-photo/portrait-white-man-isolated_53876-40306.jpg', alt: 'Sample 2' },
    { id: 3, src: 'https://th.bing.com/th/id/OIP.-1E61McENQA9ycvWgN4azQHaE8?rs=1&pid=ImgDetMain', alt: 'Sample 3' },
    { id: 4, src: 'https://thumbs.dreamstime.com/b/multiracial-group-friends-taking-selfie-urban-park-76985476.jpg', alt: 'Sample 4' }
];

const FaceDetection = () => {
    const [displayedImage, setDisplayedImage] = useState(null);

    // Hàm xử lý khi tải ảnh lên từ thiết bị
    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            setDisplayedImage(imageUrl); // Lưu URL ảnh để hiển thị
        }
    };

    // Hàm xử lý khi nhấn "Start Over"
    const handleStartOver = () => {
        setDisplayedImage(null); // Xóa URL ảnh đã hiển thị
    };

    // Hàm xử lý khi chọn ảnh mẫu
    const handleSampleImageClick = (imageUrl) => {
        setDisplayedImage(imageUrl); // Hiển thị ảnh mẫu đã chọn
    };

    return (
        <MainCard title="Face Detection Demo">
            <Typography variant="body1" sx={{ fontSize: '1rem', marginBottom: 2, whiteSpace: 'pre-line' }}>
                Face Detection allows you to find faces in an image.{"\n"}
                Along with the position of the faces, Face Detection also provides key points (eyes, nose, mouth) for each face.
            </Typography>
            <Grid container spacing={2}>
                {/* Left Side - Step 1 */}
                <Grid item xs={12} sm={6}>
                    <SubCard>
                        <Typography variant="body2" sx={{ marginBottom: 2 }}>
                            <Typography component="span" sx={{ color: 'red', fontWeight: 'bold' }}>
                                Step 1:
                            </Typography>
                            <br />
                            Select from the following sample or upload your own image
                        </Typography>

                        {/* Sample Images Section - 2x2 Grid */}
                        <Grid container spacing={2}>
                            {sampleImages.map((image) => (
                                <Grid item xs={6} key={image.id}>
                                    <Box
                                        component="img"
                                        src={image.src}
                                        alt={image.alt}
                                        onClick={() => handleSampleImageClick(image.src)} // Xử lý khi nhấp vào ảnh mẫu
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

                {/* Right Side - Result */}
                <Grid item xs={12} sm={6}>
                    <SubCard>
                        <Typography variant="body2" sx={{ marginBottom: 2 }}>
                            <Typography component="span" sx={{ color: 'red', fontWeight: 'bold' }}>
                                Result
                            </Typography>
                        </Typography>
                        <Box
                            sx={{
                                width: '100%',
                                height: 'auto',
                                backgroundColor: displayedImage ? 'transparent' : '#333', // Đặt màu nền là trong suốt khi có ảnh
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexDirection: 'column',
                                color: '#fff',
                                borderRadius: '10px',
                                overflow: 'hidden', // Đảm bảo ảnh không vượt quá kích thước khung
                                objectFit: 'cover',
                                cursor: 'pointer',
                                aspectRatio: '1 / 1',
                                marginBottom: 3,
                                marginTop: 3
                            }}
                        >
                            {!displayedImage ? (
                                <IconButton color="primary" component="label">
                                    <CloudUpload sx={{ fontSize: 60 }} />
                                    <input
                                        hidden
                                        accept="image/*"
                                        type="file"
                                        onChange={handleImageUpload}
                                    />
                                </IconButton>
                            ) : (
                                <Box
                                    component="img"
                                    src={displayedImage}
                                    alt="Displayed"
                                    sx={{
                                        width: '100%',
                                        height: '100%',
                                        objectFit: 'contain', // Đảm bảo ảnh vừa với khung mà không bị cắt
                                    }}
                                />
                            )}
                            {!displayedImage && (
                                <Typography variant="body2" sx={{ textAlign: 'center', marginTop: 1 }}>
                                    Upload Image or drag and drop in this space<br />
                                    Image should not be beyond 200x200 PX
                                </Typography>
                            )}
                        </Box>

                        {/* Nút "Start Over" */}
                        {displayedImage && (
                            <Button
                                variant="outlined"
                                color="primary"
                                onClick={handleStartOver}
                                sx={{ marginTop: 2, borderRadius: '10px' }}
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
