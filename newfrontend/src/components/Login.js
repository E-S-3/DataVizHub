import React, { useEffect, useState } from "react";
import { auth, provider, signInWithPopup, onAuthStateChanged, signOut } from "../firebaseConfig";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography, CircularProgress, Paper } from "@mui/material";
import GoogleIcon from "@mui/icons-material/Google"; // Google Icon

const Login = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        onAuthStateChanged(auth, (user) => {
            if (user) {
                setUser(user);
                navigate("/dashboard");
            } else {
                setUser(null);
            }
        });
    }, [navigate]);

    const googleSignIn = async () => {
        setLoading(true);
        try {
            const result = await signInWithPopup(auth, provider);
            const idToken = await result.user.getIdToken();

            // Send token to FastAPI backend
            await axios.post("http://127.0.0.1:8000/login", { token: idToken });

            navigate("/dashboard");
        } catch (error) {
            console.error("Error during sign-in:", error);
        }
        setLoading(false);
    };

    return (
        <Box
            sx={{
                height: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: "#f5f5f5",
            }}
        >
            <Paper
                sx={{
                    padding: 4,
                    textAlign: "center",
                    borderRadius: 3,
                    boxShadow: 5,
                    width: "100%",
                    maxWidth: 400,
                    backgroundColor: "white",
                }}
            >
                <Typography variant="h4" sx={{ fontWeight: "bold", color: "#333" }}>
                    DataVizHub
                </Typography>
                <Typography variant="subtitle1" sx={{ color: "#666", marginBottom: 3 }}>
                    Sign in to continue
                </Typography>

                {loading ? (
                    <CircularProgress />
                ) : (
                    <Button
                        variant="contained"
                        onClick={googleSignIn}
                        startIcon={<GoogleIcon />}
                        sx={{
                            backgroundColor: "#4285F4",
                            color: "white",
                            fontSize: "16px",
                            padding: "10px 20px",
                            borderRadius: "8px",
                            textTransform: "none",
                            fontWeight: "bold",
                            "&:hover": { backgroundColor: "#357ae8" },
                            width: "100%",
                        }}
                    >
                        Sign in with Google
                    </Button>
                )}
            </Paper>
        </Box>
    );
};

export default Login;
