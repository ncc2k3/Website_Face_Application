import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Typography, Button, Box } from '@mui/material';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const CustomDialog = ({ open, onClose, message }) => {
    return (
        <Dialog open={open} onClose={onClose}>
            {/* Header */}
            <DialogTitle sx={{ textAlign: 'center', padding: 2 }}>
                <ErrorOutlineIcon sx={{ fontSize: 80, color: 'red' }} />
            </DialogTitle>

            {/* Content */}
            <DialogContent sx={{ textAlign: 'center', padding: '16px 24px' }}>
                <Typography variant="h5" sx={{ fontWeight: 'bold', marginBottom: 1 }}>
                    Image uploading unsuccessful!
                </Typography>
                <Typography variant="body1" sx={{ color: '#666' }}>
                    {message}
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
