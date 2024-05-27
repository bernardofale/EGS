import PersonAddIcon from '@mui/icons-material/PersonAdd';
import { Avatar, Box, Button, Container, Paper, TextField, Typography } from '@mui/material';
import axios from 'axios';
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(''); 
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault();
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8004/register', {
        id: 0,
        username: username,
        email: email,
        full_name: fullName,
        disabled: false, 
        hashed_password: password 
      });

      if (response.status === 200) {
        navigate('/login');
      } else {
        setError('Failed to register. Please try again.');
      }
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to register. Please try again.');
    }
  };

  return (
    <Container component="main" maxWidth="xs" sx={{ mt: 8, py: 10 }}>
      <Paper elevation={3} sx={{ padding: 4 }}>
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <PersonAddIcon />
          </Avatar>
          <Typography component="h1" variant="h5" sx={{ fontSize: '1.5rem', color: '#fff' }}>
            Register
          </Typography>
          {error && (
            <Typography variant="body2" color="error" sx={{ mt: 1 }}>
              {error}
            </Typography>
          )}
          <Box component="form" onSubmit={handleRegister} sx={{ mt: 1 }}>
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
              onChange={(e) => setUsername(e.target.value)}
              InputLabelProps={{ style: { fontSize: '1.2rem' } }}
              InputProps={{ style: { fontSize: '1.2rem' } }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              InputLabelProps={{ style: { fontSize: '1.2rem' } }}
              InputProps={{ style: { fontSize: '1.2rem' } }}
            />
            <TextField
              margin="normal"
              fullWidth
              id="fullName"
              label="Full Name"
              name="fullName"
              autoComplete="name"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
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
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              InputLabelProps={{ style: { fontSize: '1.2rem' } }}
              InputProps={{ style: { fontSize: '1.2rem' } }}
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="confirmPassword"
              label="Confirm Password"
              type="password"
              id="confirmPassword"
              autoComplete="new-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
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
              Register
            </Button>
            <Typography variant="body2" align="center" color="textSecondary">
              Already have an account? <Link to="/login" style={{ color: '#1a73e8', textDecoration: 'none' }}>Login</Link>
            </Typography>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default Register;
