import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { ShieldAlert } from 'lucide-react';
import api from '../services/api';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setIsLoading(true);

    try {
      await api.post('/register', {
        username,
        password
      });

      // Automatically redirect to login page after successful registration
      navigate('/login');
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during registration');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem'
    }}>
      <div className="card animate-reveal" style={{ maxWidth: '400px', width: '100%', textAlign: 'center' }}>
        <ShieldAlert size={48} color="var(--primary-color)" style={{ marginBottom: '1.5rem' }} />
        <h2 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
          Create an <strong>Account</strong>
        </h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
          Register to access the administrator dashboard.
        </p>

        {error && <div className="error-message" style={{ marginBottom: '1.5rem' }}>{error}</div>}

        <form onSubmit={handleSignup} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input 
              className="form-control" 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
              placeholder="Enter admin username"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input 
              className="form-control" 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              placeholder="Enter password"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input 
              className="form-control" 
              type="password" 
              value={confirmPassword} 
              onChange={(e) => setConfirmPassword(e.target.value)} 
              required 
              placeholder="Confirm password"
            />
          </div>
          <button 
            type="submit" 
            className="btn btn-primary" 
            style={{ marginTop: '1rem', justifyContent: 'center' }}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div style={{ marginTop: '2rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          Already have an account?{' '}
          <Link to="/login" style={{ color: 'var(--primary-color)', textDecoration: 'none', fontWeight: 600 }}>
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Signup;
