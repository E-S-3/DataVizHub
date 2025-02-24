import React, { useEffect, useState } from "react";
import { 
  AppBar, Toolbar, Select, MenuItem, Button, TextField, 
  Box, Typography, useMediaQuery, IconButton, Drawer, CircularProgress, FormControl, FormLabel 
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { initialise } from "../service/api0";
import { useNavigate } from "react-router-dom"; //  Import for navigation
import { signOut } from "firebase/auth"; //  Import Firebase sign out
import { auth } from "../firebaseConfig"; //  Import Firebase auth


const Navbar = ({ onFilterChange }) => {
  const [department, setDepartment] = useState("");
  const [start_date, setStartDate] = useState("");
  const [end_date, setEndDate] = useState("");
  const [open, setOpen] = useState(false);

  const [loading, setLoading] = useState(true); // State to manage spinner visibility

  const navigate = useNavigate(); // ✅ Used to redirect after logout
  const isMobile = useMediaQuery("(max-width: 600px)");

  const handleApply = () => {
    onFilterChange({ department, start_date, end_date });
    setOpen(false); // Close menu after applying filters
  };

  const [departmentsList, setDepartmentsList] = useState([]);
    const [dateLimits, setDateLimits] = useState({ min: "", max: "" });
  
    useEffect(() => {
        async function fetchData() {
            const data = await initialise();
            setDepartmentsList([{ id: "", name: "All Departments" }, ...data.departments]);
            setDateLimits({ min: data.earliest_date, max: data.latest_date });
            setLoading(false);
        }
        fetchData();
    }, []);

    //  Handle Logout Function
  const handleLogout = async () => {
    await signOut(auth); // Sign out from Firebase
    navigate("/"); // Redirect to login page
  };

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        backgroundColor: "rgba(255, 255, 255, 0.8)", 
        backdropFilter: "blur(10px)", 
        boxShadow: 2, 
        padding: 1 
      }}
    >
      <Toolbar sx={{ display: "flex", justifyContent: "space-between", flexWrap: "wrap" }}>
        {/* Show spinner when loading */}
        {loading ? (
          <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", width: "100%" }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {/* Menu Button for Mobile */}
            {isMobile ? (
              <>
                <Typography variant="h6" sx={{ color: "black", fontWeight: "bold" }}>
                  DataVizHub
                </Typography>
                <IconButton onClick={() => setOpen(!open)}>
                  <MenuIcon sx={{ color: "black" }} />
                </IconButton>
              </>
            ) : (
              <Typography variant="h6" sx={{ color: "black", fontWeight: "bold" }}>
                DataVizHub
              </Typography>
            )}

            {/* Filters Section */}
            {!isMobile || open ? (
              <Box 
                sx={{ 
                  display: "flex", 
                  flexDirection: isMobile ? "column" : "row", 
                  gap: 2, 
                  alignItems: "center",
                  width: isMobile ? "100%" : "auto",
                  mt: isMobile ? 1 : 0
                }}
              >
                {/* Department Filter */}
                <FormControl sx={{ width: isMobile ? "100%" : "auto" }}>
                  <FormLabel>Filter</FormLabel>
                  <Select
                    value={department}
                    onChange={(e) => setDepartment(e.target.value)}
                    displayEmpty
                    sx={{
                      minWidth: 150,
                      backgroundColor: "white",
                      borderRadius: 1,
                      width: "100%"
                    }}
                  >
                    {departmentsList.map((dept) => (
                      <MenuItem key={dept.id} value={dept.id}>
                        {dept.name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                {/* Start Date Filter with Label outside the TextField */}
                <FormControl sx={{ width: isMobile ? "100%" : "auto" }}>
                  <FormLabel>Start Date</FormLabel>
                  <TextField
                    type="date"
                    value={start_date}
                    onChange={(e) => setStartDate(e.target.value)}
                    inputProps={{ min: dateLimits.min, max: dateLimits.max }}
                    sx={{
                      backgroundColor: "white",
                      borderRadius: 1,
                      width: "100%"
                    }}
                  />
                </FormControl>

                {/* End Date Filter with Label outside the TextField */}
                <FormControl sx={{ width: isMobile ? "100%" : "auto" }}>
                  <FormLabel>End Date</FormLabel>
                  <TextField
                    type="date"
                    value={end_date}
                    onChange={(e) => setEndDate(e.target.value)}
                    inputProps={{ min: dateLimits.min, max: dateLimits.max }}
                    sx={{
                      backgroundColor: "white",
                      borderRadius: 1,
                      width: "100%"
                    }}
                  />
                </FormControl>

                {/* Apply Button */}
                <Button
                  variant="contained"
                  onClick={handleApply}
                  sx={{ width: isMobile ? "100%" : "auto" }}
                >
                  Apply
                </Button>

                {/* Logout Button */}
                <Button variant="contained" color="error" onClick={handleLogout} sx={{ width: isMobile ? "100%" : "auto" }}>Logout</Button>
              </Box>
            ) : null}
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;