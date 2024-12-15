/* eslint-disable no-unused-vars */
import { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

// material-ui
import { useTheme } from '@mui/material/styles';
import {
  Box,
  Button,
  Checkbox,
  Divider,
  FormControl,
  FormControlLabel,
  FormHelperText,
  Grid,
  IconButton,
  InputAdornment,
  InputLabel,
  OutlinedInput,
  TextField,
  Typography,
  useMediaQuery
} from '@mui/material';

// third party
import * as Yup from 'yup';
import { Formik } from 'formik';

// project imports
import useScriptRef from 'hooks/useScriptRef';
import Google from 'assets/images/icons/social-google.svg';
import AnimateButton from 'ui-component/extended/AnimateButton';
import { strengthColor, strengthIndicator } from 'utils/password-strength';

// assets
import Visibility from '@mui/icons-material/Visibility';
import VisibilityOff from '@mui/icons-material/VisibilityOff';

import axios from 'axios';
import Webcam from 'react-webcam';
import { useNavigate } from 'react-router-dom';
import { callApi } from 'utils/apiHelper';
import { API_CONFIG } from 'apiConfig';

const FirebaseRegister = ({ ...others }) => {
  const theme = useTheme();
  const scriptedRef = useScriptRef();
  const matchDownSM = useMediaQuery(theme.breakpoints.down('md'));
  const customization = useSelector((state) => state.customization);
  const [showPassword, setShowPassword] = useState(false);
  const [checked, setChecked] = useState(true);
  const [strength, setStrength] = useState(0);
  const [level, setLevel] = useState();
  const [loading, setLoading] = useState(false);   // Quản lý trạng thái "Processing"
  const [processingDone, setProcessingDone] = useState(false); // Trạng thái khi đã xử lý xong
  const [imageSrc, setImageSrc] = useState(null);  // Lưu ảnh đã chụp
  const webcamRef = useRef(null);  // Webcam



  const googleHandler = async () => {
    console.error('Register');
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  const changePassword = (value) => {
    const temp = strengthIndicator(value);
    setStrength(temp);
    setLevel(strengthColor(temp));
  };

  const navigate = useNavigate();
  // Trong hàm handleSignUp:
  const handleSignUp = (values) => {
    try {
      const response = callApi(API_CONFIG.ENDPOINTS.REGISTER, {
        first_name: values.first_name,
        last_name: values.last_name,
        email: values.email,
        password: values.password
      });
      console.log(response.data);
      alert('User registered successfully');
      // Chuyển hướng sang trang đăng ký Face ID
      navigate(`/pages/register/register-face-id?email=${values.email}`); // Gửi email thông qua query params
    } catch (error) {
      console.log(error);
      alert('Email already exists', error);
    }
  };


  // Hàm chụp ảnh từ webcam và gửi ảnh đến backend để đăng ký Face ID
  const handleRegisterWithFaceID = async (email) => {
    setLoading(true);  // Hiển thị trạng thái "Processing..."
    const capturedImage = webcamRef.current.getScreenshot();  // Chụp ảnh từ webcam

    if (capturedImage) {
      const imageBlob = dataURLtoBlob(capturedImage);  // Chuyển base64 sang blob
      const formData = new FormData();
      formData.append('image', imageBlob, 'face_image.jpg');  // Tạo form-data để gửi file ảnh
      formData.append('email', email);  // Gửi email

      try {
        const response = await axios.post('http://localhost:8800/auth/register_face', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.status === 200) {
          alert('Face ID registered successfully!');
          setImageSrc(capturedImage);  // Lưu lại ảnh đã chụp sau khi đăng ký thành công
          setProcessingDone(true);     // Đánh dấu quá trình xử lý đã xong
        } else {
          alert(`Failed to register Face ID: ${response.data.message}`);
        }
      } catch (error) {
        console.error('Error during Face ID registration:', error.response ? error.response.data : error.message);
        alert('An error occurred during registration.');
      } finally {
        setLoading(false);  // Kết thúc trạng thái "Processing"
      }
    } else {
      alert('Failed to capture image from webcam');
      setLoading(false);
    }
  };

  // Hàm reset để chụp lại ảnh
  const handleReset = () => {
    setImageSrc(null);         // Xóa ảnh đã chụp
    setProcessingDone(false);  // Đặt lại trạng thái để có thể chụp lại
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

  useEffect(() => {
    changePassword('123456');
  }, []);

  return (
    <>
      <Grid container direction="column" justifyContent="center" spacing={2}>
        <Grid item xs={12} container alignItems="center" justifyContent="center">
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle1">Sign up with Email address</Typography>
          </Box>
        </Grid>
      </Grid>

      <Formik
        initialValues={{
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          submit: null
        }}
        validationSchema={Yup.object().shape({
          first_name: Yup.string().max(255).required('First Name is required'), // Kiểm tra first_name
          last_name: Yup.string().max(255).required('Last Name is required'),   // Kiểm tra last_name
          email: Yup.string().email('Must be a valid email').max(255).required('Email is required'),
          password: Yup.string().max(255).required('Password is required')
        })}
        onSubmit={async (values, { setErrors, setStatus, setSubmitting }) => {
          try {
            if (scriptedRef.current) {
              handleSignUp(values); // Gọi handleSignUp với các giá trị từ Formik
              setStatus({ success: true });
              setSubmitting(false);
            }
          } catch (err) {
            console.error(err);
            if (scriptedRef.current) {
              setStatus({ success: false });
              setErrors({ submit: err.message });
              setSubmitting(false);
            }
          }
        }}
      >
        {({ errors, handleBlur, handleChange, handleSubmit, isSubmitting, touched, values }) => (
          <form noValidate onSubmit={handleSubmit} {...others}>
            <Grid container spacing={matchDownSM ? 0 : 2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="First Name"
                  margin="normal"
                  name="first_name"
                  type="text"
                  value={values.first_name}
                  onBlur={handleBlur}
                  onChange={handleChange}
                  error={Boolean(touched.first_name && errors.first_name)}
                  helperText={touched.first_name && errors.first_name}
                  sx={{ ...theme.typography.customInput }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Last Name"
                  margin="normal"
                  name="last_name"
                  type="text"
                  value={values.last_name}
                  onBlur={handleBlur}
                  onChange={handleChange}
                  error={Boolean(touched.last_name && errors.last_name)}
                  helperText={touched.last_name && errors.last_name}
                  sx={{ ...theme.typography.customInput }}
                />
              </Grid>
            </Grid>
            <FormControl fullWidth error={Boolean(touched.email && errors.email)} sx={{ ...theme.typography.customInput }}>
              <InputLabel htmlFor="outlined-adornment-email-register">Email Address / Username</InputLabel>
              <OutlinedInput
                id="outlined-adornment-email-register"
                type="email"
                value={values.email}
                name="email"
                onBlur={handleBlur}
                onChange={handleChange}
              />
              {touched.email && errors.email && (
                <FormHelperText error id="standard-weight-helper-text--register">
                  {errors.email}
                </FormHelperText>
              )}
            </FormControl>

            <FormControl fullWidth error={Boolean(touched.password && errors.password)} sx={{ ...theme.typography.customInput }}>
              <InputLabel htmlFor="outlined-adornment-password-register">Password</InputLabel>
              <OutlinedInput
                id="outlined-adornment-password-register"
                type={showPassword ? 'text' : 'password'}
                value={values.password}
                name="password"
                label="Password"
                onBlur={handleBlur}
                onChange={(e) => {
                  handleChange(e);
                  changePassword(e.target.value);
                }}
                endAdornment={
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handleClickShowPassword}
                      onMouseDown={handleMouseDownPassword}
                      edge="end"
                      size="large"
                    >
                      {showPassword ? <Visibility /> : <VisibilityOff />}
                    </IconButton>
                  </InputAdornment>
                }
              />
              {touched.password && errors.password && (
                <FormHelperText error id="standard-weight-helper-text-password-register">
                  {errors.password}
                </FormHelperText>
              )}
            </FormControl>

            {strength !== 0 && (
              <FormControl fullWidth>
                <Box sx={{ mb: 2 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item>
                      <Box style={{ backgroundColor: level?.color }} sx={{ width: 85, height: 8, borderRadius: '7px' }} />
                    </Grid>
                    <Grid item>
                      <Typography variant="subtitle1" fontSize="0.75rem">
                        {level?.label}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>
              </FormControl>
            )}

            <Grid container alignItems="center" justifyContent="space-between">
              <Grid item>
                <FormControlLabel
                  control={
                    <Checkbox checked={checked} onChange={(event) => setChecked(event.target.checked)} name="checked" color="primary" />
                  }
                  label={
                    <Typography variant="subtitle1">
                      Agree with &nbsp;
                      <Typography variant="subtitle1" component={Link} to="#">
                        Terms & Condition.
                      </Typography>
                    </Typography>
                  }
                />
              </Grid>
            </Grid>
            {errors.submit && (
              <Box sx={{ mt: 3 }}>
                <FormHelperText error>{errors.submit}</FormHelperText>
              </Box>
            )}

            <Box sx={{ mt: 2 }}>
              <AnimateButton>
                <Button
                  disableElevation
                  disabled={isSubmitting}
                  fullWidth
                  size="large"
                  type="submit"
                  variant="contained"
                  color="secondary"
                >
                  Sign up
                </Button>
              </AnimateButton>
            </Box>
          </form>
        )}
      </Formik>
    </>
  );
};

export default FirebaseRegister;
