import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Typography, Button } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const CustomDialog = ({ open, onClose }) => {
    return (
        <Dialog 
            open={open} 
            onClose={onClose}
            PaperProps={{
                sx: {
                    padding: 3,
                    height: 'auto', // Chiều cao tự động
                    width: '600px', // Chiều rộng cụ thể
                    textAlign: 'center',
                    border: '3px solid black', // Viền màu đen
                    borderRadius: '8px', // Tùy chỉnh bo góc
                },
            }}
        >
            {/* Header */}
            <DialogTitle sx={{ textAlign: 'center', padding: 2 }}>
                <ErrorOutlineIcon sx={{ fontSize: 100, color: 'red' }} />
            </DialogTitle>

            {/* Content */}
            <DialogContent sx={{ textAlign: 'center', padding: '24px 24px' }}>
                <Typography variant="h2" sx={{ fontWeight: 'bold', marginBottom: 1, fontSize: '35px' }}>
                    Image uploading unsuccessful!
                </Typography>
                <Typography variant="body1" sx={{ color: '#666' , fontSize: '20px'}}>
                    Could not obtain at least one face from <br /> the supplied image(s)
                </Typography>
            </DialogContent>

            {/* Actions */}
            <DialogActions sx={{ justifyContent: 'center', paddingBottom: 2 }}>
                <Button
                    onClick={onClose}
                    variant="contained"
                    sx={{
                        background: 'linear-gradient(to right, #ff7e5f, #feb47b)',
                        color: '#fff',
                        fontWeight: 'bold',
                        fontSize: '15px',
                        padding: '10px 20px',
                        borderRadius: '8px',
                        textTransform: 'none',
                        '&:hover': {
                            background: 'linear-gradient(to right, #feb47b, #ff7e5f)',
                        },
                    }}
                >
                    Try again
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default CustomDialog;
