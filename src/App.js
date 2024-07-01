import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import HomePage from './components/home';
import Login from './components/auth';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    () => JSON.parse(localStorage.getItem('isAuthenticated')) || false
  );

  const handleLogin = () => {
    setIsAuthenticated(true);
    localStorage.setItem('isAuthenticated', JSON.stringify(true));
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('isAuthenticated');
  };

  useEffect(() => {
    console.log("isAuthenticated:", isAuthenticated);
  }, [isAuthenticated]);

  return (
    <Router>
      <Switch>
        <Route path="/login">
          {isAuthenticated ? <Redirect to="/home" /> : <Login onLogin={handleLogin} />}
        </Route>
        <Route path="/home">
          {isAuthenticated ? <HomePage onLogout={handleLogout} /> : <Redirect to="/login" />}
        </Route>
        <Redirect from="/" to={isAuthenticated ? "/home" : "/login"} />
      </Switch>
    </Router>
  );
}

export default App;


