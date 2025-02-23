import React, { useEffect, useState } from "react";
import { 
  AppBar, Toolbar, Select, MenuItem, Button, TextField, 
  Box, Typography, useMediaQuery, IconButton, Drawer 
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { initialise } from "../service/api0";


const Navbar = ({ onFilterChange }) => {
  const [department, setDepartment] = useState("");
  const [start_date, setStartDate] = useState("");
  const [end_date, setEndDate] = useState("");
  const [open, setOpen] = useState(false);

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
        }
        fetchData();
    }, []);

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
        {/* Menu Button for Mobile */}
        {isMobile ? (
            <>
            <Typography variant="h6" sx={{ color: "black", fontWeight: "bold" }}>
            Dashboard Filters
          </Typography>
          <IconButton onClick={() => setOpen(!open)}>
            <MenuIcon sx={{ color: "black" }} />
          </IconButton>
            </>
          
        ) : (
          <Typography variant="h6" sx={{ color: "black", fontWeight: "bold" }}>
            Dashboard Filters
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
            <Select
                value={department}
                onChange={(e) => setDepartment(e.target.value)}
                displayEmpty
                sx={{
                    minWidth: 150,
                    backgroundColor: "white",
                    borderRadius: 1,
                    width: isMobile ? "100%" : "auto"
                }}
            >
                {departmentsList.map((dept) => (
                    <MenuItem key={dept.id} value={dept.id}>
                        {dept.name}
                    </MenuItem>
                ))}
            </Select>

            <TextField
                type="date"
                value={start_date}
                onChange={(e) => setStartDate(e.target.value)}
                inputProps={{ min: dateLimits.min, max: dateLimits.max }}
                sx={{
                    backgroundColor: "white",
                    borderRadius: 1,
                    width: isMobile ? "100%" : "auto"
                }}
            />

            <TextField
                type="date"
                value={end_date}
                onChange={(e) => setEndDate(e.target.value)}
                inputProps={{ min: dateLimits.min, max: dateLimits.max }}
                sx={{
                    backgroundColor: "white",
                    borderRadius: 1,
                    width: isMobile ? "100%" : "auto"
                }}
            />

            <Button 
              variant="contained" 
              onClick={handleApply} 
              sx={{ width: isMobile ? "100%" : "auto" }}
            >
              Apply
            </Button>
          </Box>
        ) : null}
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
