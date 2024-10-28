import React, { useEffect, useRef, useState } from 'react';
import * as faceapi from 'face-api.js';
import axios from 'axios';

const FaceID = ({ mode }) => {
    const videoRef = useRef(null);
    const [isModelLoaded, setModelLoaded] = useState(false);
    const [isFaceDetected, setFaceDetected] = useState(false);

    // Load models from face-api.js
    useEffect(() => {
        const loadModels = async () => {
            const MODEL_URL = '/models';
            await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
            await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
            await faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL);
            setModelLoaded(true);
        };

        loadModels();
    }, []);

    // Start video stream
    const startVideo = () => {
        navigator.getUserMedia(
            { video: {} },
            (stream) => (videoRef.current.srcObject = stream),
            (err) => console.error(err)
        );
    };

    // Detect face from the video stream
    const handleVideoPlay = async () => {
        const video = videoRef.current;
        const canvas = faceapi.createCanvasFromMedia(video);
        document.body.append(canvas);

        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);

        setInterval(async () => {
            const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceDescriptors();
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
            faceapi.draw.drawDetections(canvas, detections);
            faceapi.draw.drawFaceLandmarks(canvas, detections);

            // Check if any face is detected
            if (detections.length > 0) {
                setFaceDetected(true);

                if (mode === 'register') {
                    handleRegister(detections[0].descriptor);
                } else if (mode === 'login') {
                    handleLogin(detections[0].descriptor);
                }
            } else {
                setFaceDetected(false);
            }
        }, 100);
    };

    // Handle registration
    const handleRegister = async (faceDescriptor) => {
        try {
            const response = await axios.post('http://localhost:5000/api/register', { faceDescriptor });
            console.log(response.data.message);
        } catch (error) {
            console.error(error);
        }
    };

    // Handle login
    const handleLogin = async (faceDescriptor) => {
        try {
            const response = await axios.post('http://localhost:5000/api/login', { faceDescriptor });
            if (response.data.success) {
                alert('Login successful');
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <video ref={videoRef} onPlay={handleVideoPlay} width="720" height="560" autoPlay muted />
            {!isModelLoaded && <p>Loading face detection models...</p>}
            {!isFaceDetected && <p>No face detected. Please look at the camera.</p>}
        </div>
    );
};

export default FaceID;
