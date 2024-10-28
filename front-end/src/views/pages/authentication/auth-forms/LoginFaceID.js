// LoginWithFaceID.js
import { useRef, useState } from 'react';
import { Button } from '@mui/material';
import Webcam from 'react-webcam';
import axios from 'axios';
import { useNavigate } from 'react-router';
import { Grid, Typography } from '@mui/material';

const LoginWithFaceID = () => {
    const webcamRef = useRef(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const dataURLtoBlob = (dataurl) => {
        let arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
            bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
    };

    const handleLoginWithFaceID = async () => {
        setLoading(true);

        const imageSrc = webcamRef.current.getScreenshot();
        if (imageSrc) {
            const imageBlob = dataURLtoBlob(imageSrc);
            const formData = new FormData();
            formData.append('image', imageBlob, 'face_image.jpg');

            try {
                const response = await axios.post('http://localhost:8800/auth/login_face', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                if (response.status === 200) {
                    if (response.data.message === 'Login successful') {
                        alert('Face ID login successful!');
                        navigate('/');
                    } else {
                        alert(`${response.data.message}`);
                    }
                }
            } catch (error) {
                console.error('Error during Face ID login:', error);
                alert('An error occurred during login.');
            } finally {
                setLoading(false);
            }
        } else {
            alert('Failed to capture image from webcam');
            setLoading(false);
        }
    };

    return (
        <Grid container direction="column" justifyContent="center" alignItems="center" spacing={2}>
            <Grid item xs={12}>
                <Typography  variant="h1" sx={{ mt: 2, mb: 2, textAlign: 'center' }} align="center">Login with Face ID</Typography>
            </Grid>
            <Grid item xs={12}>
                <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width={720}
                    height={560}
                />
            </Grid>
            <Grid item xs={12}>
                <Button
                    variant="contained"
                    onClick={handleLoginWithFaceID}
                    disabled={loading}
                    fullWidth
                    sx={{ mt: 2 }}
                    size = "large"
                >
                    {loading ? 'Processing...' : 'Login with Face ID'}
                </Button>
            </Grid>
        </Grid>
    );
};

export default LoginWithFaceID;
