import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import { createUserWithEmailAndPassword, signInWithPopup, signInWithEmailAndPassword } from 'firebase/auth';
import { googleprovider } from '../config/firebase-config';
import { auth } from '../config/firebase-config';
import './auth.css';
function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSignUp, setIsSignUp] = useState(false);
  const history = useHistory();

  const signIn = async () => {
    try {
      await signInWithEmailAndPassword(auth, email, password);
      console.log('Successfully logged in');
      onLogin();
      history.push('/home');
    } catch (error) {
      console.error('Error logging in:', error.message);
    }
  };

  const signUp = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      console.log('Successfully signed up');
      history.push('./');
    } catch (error) {
      console.error('Error signing up:', error.message);
    }
  };

  const signInWithGoogle = async () => {
    try {
      await signInWithPopup(auth, googleprovider);
      console.log('Successfully signed in with Google');
      onLogin();
      history.push('/home');
    } catch (error) {
      console.error('Error signing in with Google:', error.message);
    }
  };

  const handleAuthAction = () => {
    if (isSignUp) {
      signUp();
    } else {
      signIn();
    }
  };

  const toggleAuthMode = () => {
    setIsSignUp((prev) => !prev);
  };

  return (
    <div className="login-container">
       <div className="welcome-message">
        <h1>Welcome to Fi-chatbot</h1>
        <h3>- ask anything related to company stocks and loans</h3> 
      </div>
      <div className="login-form">
        <h2>{isSignUp ? 'Sign Up' : 'Login'}</h2>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
  
        <button onClick={handleAuthAction}>
          {isSignUp ? 'Sign Up' : 'Log In'}
        </button>
        <p>
          {isSignUp
            ? 'Already have an account?'
            : 'Don\'t have an account yet?'}
          <button onClick={toggleAuthMode}>
            {isSignUp ? 'Log In' : 'Sign Up'}
          </button>
          <button onClick={signInWithGoogle}>Sign in with Google</button>
        </p>
      </div>
     
    </div>
  );
}

export default Login;
