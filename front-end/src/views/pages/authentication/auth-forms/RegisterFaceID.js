import { useNavigate, useLocation } from 'react-router-dom';
import { useState, useRef } from 'react';
import { Button, Typography, Grid } from '@mui/material';
import Webcam from 'react-webcam';
// import axios from 'axios';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

const RegisterFaceID = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const webcamRef = useRef(null);
    const [loading, setLoading] = useState(false);
    const [processingDone, setProcessingDone] = useState(false);
    const [imageSrc, setImageSrc] = useState(null);

    // Lấy email từ URL query params
    const params = new URLSearchParams(location.search);
    const email = params.get('email'); // Lấy email từ query params

    // Kiểm tra email có tồn tại không
    if (!email) {
        alert('No email provided');
        // navigate('/');  // Chuyển về trang chủ nếu không có email
        return null;
    }

    // Hàm chụp ảnh từ webcam và gửi ảnh đến backend để đăng ký Face ID
    const handleRegisterWithFaceID = async () => {
        setLoading(true);
        const capturedImage = webcamRef.current.getScreenshot();

        if (capturedImage) {
            const imageBlob = dataURLtoBlob(capturedImage);
            const formData = new FormData();
            formData.append('image', imageBlob, 'face_image.jpg');
            formData.append('email', email);  // Gửi email

            try {
                const response = await callApi(API_CONFIG.ENDPOINTS.REGISTER_FACE, formData, true);

                if (response.status === 200) {
                    alert('Face ID registered successfully!');
                    setImageSrc(capturedImage);
                    setProcessingDone(true);


                    navigate('/pages/login/login3');  // Chuyển về đăng nhập
                } else {
                    alert(`Failed to register Face ID: ${response.data.message}`);
                }
            } catch (error) {
                console.error('Error during Face ID registration:', error.response ? error.response.data : error.message);
                alert('Faced is not detected. Please try again.');
            } finally {
                setLoading(false);
            }
        } else {
            alert('Failed to capture image from webcam');
            setLoading(false);
        }
    };

    // Hàm chuyển base64 sang blob để gửi file ảnh
    const dataURLtoBlob = (dataurl) => {
        let arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
    };

    return (
        <Grid container direction="column" justifyContent="center" alignItems="center" spacing={2}>
            {/* Hiển thị ảnh đã chụp */}
            <Grid item xs={12}>
                {imageSrc && processingDone ? (
                    <>
                        <Typography variant="h6">Captured Image</Typography>
                        <img src={imageSrc} alt="Captured" width={720} height={560} style={{ marginTop: '16px' }} />
                    </>
                ) : (
                    <>
                        <Typography variant="h1" sx={{ mt: 2, mb: 2, textAlign: 'center' }}>Register Face ID</Typography>
                        <Webcam
                            audio={false}
                            ref={webcamRef}
                            screenshotFormat="image/jpeg"
                            width={720}
                            height={560}
                        />
                    </>
                )}
            </Grid>

            {/* Nút đăng ký Face ID */}
            <Grid item xs={12}>
                <Button
                    variant="contained"
                    onClick={handleRegisterWithFaceID}
                    disabled={loading || processingDone}
                    fullWidth
                    size="large" // Sử dụng kích thước lớn
                >
                    {loading ? 'Processing...' : 'Register Face ID'}
                </Button>
            </Grid>
        </Grid>
    );
};

export default RegisterFaceID;
