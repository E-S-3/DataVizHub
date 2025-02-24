import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import Dashboard from "./Dashboard";
import Login from "./components/Login";
import Security from "./components/Security";

import { auth, onAuthStateChanged } from "./firebaseConfig";

const ProtectedRoute = ({ children }) => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    onAuthStateChanged(auth, (user) => {
      if (!user) {
        navigate("/"); // Redirect to login if user is not signed in
      } else {
        setUser(user);
      }
      setLoading(false);
    });
  }, [navigate]);

  if (loading) return <p>Loading...</p>; // Show a loading state while checking auth

  return children;
};

function App() {
  return (
    <>
    <Security />
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      </Routes>
    </Router>
    </>
  );
}

export default App;
