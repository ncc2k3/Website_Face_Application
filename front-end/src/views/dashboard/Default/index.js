import React from 'react';
import { Box } from '@mui/material';

const Dashboard = () => {
  const firstName = localStorage.getItem('firstName') || '';
  const lastName = localStorage.getItem('lastName') || '';
  const text = `Hello, ${firstName + ' ' + lastName || 'Guest'}!`;
  const text1 = "Welcome to my face application.";
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        height: '500px',
        backgroundImage: 'url("/path/to/your/background.jpg")', // Replace with your image path
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        color: 'black',
        textAlign: 'center',
        // overflow: 'hidden',
        flexDirection: 'column', // Set the layout to column to handle multi-line text
      }}
    >
      <Box
        sx={{
          display: 'inline-flex',
          fontWeight: 'bold',
          marginTop: '100px', // Add spacing between the lines
          fontSize: '48px',
          textShadow: '2px 2px 4px rgba(0, 0, 0, 0.5)',
          '@keyframes wave': {
            '0%, 100%': { transform: 'translateY(0)' },
            '50%': { transform: 'translateY(-15px)' },
          },
        }}
      >
        {text.split("").map((char, index) => (
          <Box
            key={index}
            component="span"
            sx={{
              display: 'inline-block',
              animation: `wave 1.5s infinite`,
              animationDelay: `${index * 0.1}s`, // Delay for each letter
            }}
          >
            {char === " " ? "\u00A0" : char} {/* Handle spaces */}
          </Box>
        ))}
      </Box>
      <Box
        sx={{
          display: 'inline-flex',
          fontWeight: 'bold',
          fontSize: '48px',
          marginTop: '100px', // Add spacing between the lines
          textShadow: '1px 1px 2px rgba(0, 0, 0, 0.5)',
        }}
      >
        {text1.split("").map((char, index) => (
          <Box
            key={index}
            component="span"
            sx={{
              display: 'inline-block',
              animation: `wave 1.5s infinite`,
              animationDelay: `${(index + text.length) * 0.1}s`, // Delay for each letter
            }}
          >
            {char === " " ? "\u00A0" : char} {/* Handle spaces */}
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default Dashboard;
