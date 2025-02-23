import React, { useEffect, useState } from "react";
import { Grid, Card, CardContent, Typography, Box } from "@mui/material";
import ReactApexChart from "react-apexcharts";
import Navbar from "./components/Navbar";
import { fetchPieChartData } from "./service/api1";


function App() {
  const [filters, setFilters] = useState({ department: "", start_date: "", end_date: "" });
  const [pieChartData, setPieChartData] = useState({ labels: [], values: [] });

  useEffect(() => {
    async function getData() {
      const data = await fetchPieChartData(filters);
      console.log("Pie Chart Data:", data);
      setPieChartData({ labels: data.labels, values: data.values });
    }
    getData();
  }, [filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    console.log("Filters Applied:", newFilters);
    // API Calls can be triggered here for each graph using the new filter values
  };

  const pieChartOptions = {
    chart: { type: "pie"},
    legend: {
      position: 'bottom'
  }
  };

  const barChartOptions = {
    chart: { type: "bar" },
    xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] },
  };

  const lineChartOptions = {
    chart: { type: "line" },
    xaxis: { categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] },
  };

  

  return (
    <>
    <Navbar onFilterChange={handleFilterChange} />
    <Box p={3} mt={10}>
      <Grid container spacing={3} justifyContent="center" alignItems="center" >
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "450px" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Task Distribution</Typography>
              <ReactApexChart
                options={{ 
                  chart: { type: "pie" }, 
                  legend: {
                    position: 'bottom'
                  }, 
                  labels: pieChartData.labels 
              }}
                series={pieChartData.values}
                type="pie"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "450px" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Website Views</Typography>
              <ReactApexChart
                options={barChartOptions}
                series={[{ data: [65, 59, 80, 81, 56, 55] }]}
                type="bar"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "450px" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Daily Sales</Typography>
              <ReactApexChart
                options={lineChartOptions}
                series={[
                  { name: "Daily Sales", data: [10, 20, 30, 40, 50, 60] },
                  { name: "Completed Tasks", data: [5, 15, 25, 35, 45, 55] }
                ]}
                type="line"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "450px" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Daily Sales</Typography>
              <ReactApexChart
                options={lineChartOptions}
                series={[
                  { name: "Daily Sales", data: [10, 20, 30, 40, 50, 60] },
                  { name: "Completed Tasks", data: [5, 15, 25, 35, 45, 55] }
                ]}
                type="line"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "450px" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Daily Sales</Typography>
              <ReactApexChart
                options={lineChartOptions}
                series={[
                  { name: "Daily Sales", data: [10, 20, 30, 40, 50, 60] },
                  { name: "Completed Tasks", data: [5, 15, 25, 35, 45, 55] }
                ]}
                type="line"
              />
            </CardContent>
          </Card>
        </Grid>        
      </Grid>
    </Box>
    </>
  );
}

export default App;
