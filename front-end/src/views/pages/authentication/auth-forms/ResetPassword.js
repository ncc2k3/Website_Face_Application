/* eslint-disable no-unused-vars */

import React, { useState } from 'react';
import axios from 'axios';
import { Typography, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button, TextField, Box } from '@mui/material';

const ForgotPassword = () => {
    const [openDialog, setOpenDialog] = useState(false);
    const [email, setEmail] = useState("");
    const [confirmationOpen, setConfirmationOpen] = useState(false);
    const [responseMessage, setResponseMessage] = useState(""); // Thêm state để lưu thông báo phản hồi từ API

    // Hàm mở hộp thoại xác nhận
    const handleForgotPasswordClick = () => {
        alert('Reset Password? Not implemented yet!');
        setOpenDialog(false);
    };

    // Hàm khi nhấn nút "Có"
    const handleConfirmReset = () => {
        setConfirmationOpen(false);
        axios
            .post('http://localhost:8800/auth/reset_password', { email })
            .then(response => {
                setResponseMessage(response.data.message);  // Lưu phản hồi từ backend vào state
                alert(response.data.message);  // Thông báo thành công
            })
            .catch(error => {
                setResponseMessage("There was an error!");  // Thông báo lỗi
                alert('There was an error!');  // Thông báo lỗi
            });
    };

    // Đóng hộp thoại xác nhận
    const handleCloseDialog = () => {
        setOpenDialog(false);
    };

    // Hàm hiển thị form xác nhận gửi yêu cầu reset password
    const handleOpenConfirmation = () => {
        setConfirmationOpen(true);
        setOpenDialog(false);  // Đóng form nhập email
    };

    return (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh" flexDirection="column">
            {/* Nút "Reset Password?" */}
            <Typography
                variant="h1" // Đặt chữ to hơn
                color="secondary"
                fullWidth
                size="large"
                sx={{ textDecoration: 'none', cursor: 'pointer', mb: 2 }}
                onClick={handleForgotPasswordClick}
            >
                Reset Password?
            </Typography>

            {/* Form nhập email */}
            <Dialog open={openDialog} onClose={handleCloseDialog}>
                <DialogTitle>Reset Password</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Please enter your email to reset the password.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="email"
                        label="Email Address"
                        type="email"
                        fullWidth
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDialog}>Cancel</Button>
                    <Button onClick={handleOpenConfirmation}>Reset Password</Button>
                </DialogActions>
            </Dialog>

            {/* Form xác nhận có chắc chắn muốn reset password không */}
            <Dialog
                open={confirmationOpen}
                onClose={() => setConfirmationOpen(false)}
                aria-labelledby="confirm-reset-dialog-title"
                aria-describedby="confirm-reset-dialog-description"
            >
                <DialogTitle id="confirm-reset-dialog-title">{"Confirm Reset Password"}</DialogTitle>
                <DialogContent>
                    <DialogContentText id="confirm-reset-dialog-description">
                        Are you sure you want to reset the password for {email}?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setConfirmationOpen(false)} color="primary">
                        No
                    </Button>
                    <Button onClick={handleConfirmReset} color="primary" autoFocus>
                        Yes
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Hiển thị thông báo phản hồi */}
            {responseMessage && (
                <Typography variant="subtitle1" color="primary" sx={{ mt: 2 }}>
                    {responseMessage}
                </Typography>
            )}
        </Box>
    );
};

export default ForgotPassword;
