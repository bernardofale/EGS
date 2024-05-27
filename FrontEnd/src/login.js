import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { Avatar, Box, Button, Container, Paper, TextField, Typography } from '@mui/material';
import Cookies from 'js-cookie';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ setIsAuthenticated }) => {
  const [username, SetUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();

    const headers = {
      'accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    };

    const data = new URLSearchParams();
    data.append('grant_type', '');
    data.append('username', username);
    data.append('password', password);
    data.append('scope', '');
    data.append('client_id', '');
    data.append('client_secret', '');

    try {
      const response = await fetch('http://localhost:8004/login', {
        method: 'POST',
        headers: headers,
        body: data
      });

      if (response.ok) {
        const responseData = await response.json();
        const accessToken = responseData.access_token;
        Cookies.set('access_token', accessToken, { expires: 7 });
        setIsAuthenticated(true);
        navigate('/dashboard');
      } else {
        console.error('Authentication failed');
      }
    } catch (error) {
      console.error('Error during authentication:', error);
    }
  };

  return (
    <Container component="main" maxWidth="xs" sx={{ mt: 8, py: 20 }}>
      <Paper elevation={3} sx={{ padding: 4 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5" sx={{ fontSize: '1.5rem', color: '#fff' }}>
            Login
          </Typography>
          <Box component="form" onSubmit={handleLogin} sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={username}
              onChange={(e) => SetUsername(e.target.value)}
              InputLabelProps={{ style: { fontSize: '1.2rem' } }}
              InputProps={{ style: { fontSize: '1.2rem' } }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              InputLabelProps={{ style: { fontSize: '1.2rem' } }}
              InputProps={{ style: { fontSize: '1.2rem' } }}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              sx={{ mt: 3, mb: 2, fontSize: '1rem' }}
            >
              Login
            </Button>
            <Typography variant="body2" align="center" color="textSecondary">
              Don't have an account? <Link to="/register" style={{ color: '#1a73e8', textDecoration: 'none' }}>Register</Link>
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Login;
