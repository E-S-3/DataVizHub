import React, { useEffect, useState } from "react";
import { Grid, Card, CardContent, Typography, Box } from "@mui/material";
import ReactApexChart from "react-apexcharts";
import Navbar from "./components/Navbar";
import { fetchPieChartData } from "./service/api1";
import { fetchBarChartData } from "./service/api2";
import { fetchLineChartData } from "./service/api3";
import { fetchNetBarChartData } from "./service/api5";


function App() {
  const [filters, setFilters] = useState({ department: "", start_date: "", end_date: "" });
  const [pieChartData, setPieChartData] = useState({ labels: [], values: [] });
  const [barChartData, setBarChartData] = useState({ labels: [], values: [] });
  const [lineChartData, setLineChartData] = useState({ labels: [], series: [] });
  const [netBarChartData, setnetBarChartData] = useState({ labels: [], series: [] });


  useEffect(() => {
    async function getData() {
      const piePromise = fetchPieChartData(filters);
      const barPromise = fetchBarChartData(filters);
      const linePromise = fetchLineChartData(filters);
      const netBarPromise = fetchNetBarChartData(filters);

      // Wait for all promises to resolve (they run simultaneously)
      const [pieData, barData, lineData, netBarData] = await Promise.all([piePromise, barPromise, linePromise, netBarPromise]);

      
      setPieChartData({ labels: pieData.labels, values: pieData.values });
      setBarChartData({ labels: barData.labels, values: barData.values });
      setLineChartData({
        labels: lineData.years, // X-axis (Years)
        series: [
            { name: "Revenues", data: lineData.revenues },
            { name: "Expenses", data: lineData.expenses }
        ]
      });
      setnetBarChartData({ labels: netBarData.times, values: netBarData.net_profits });

    }
    getData();
  }, [filters]);

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const pieChartOptions = {
    chart: { type: "pie"},
    legend: {
      position: 'bottom'
  }
  };

  const barChartOptions = {
    chart: { type: "bar" }
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
              height: { xs: "auto", lg: "auto" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Task Distribution</Typography>
              <ReactApexChart
                options={{ 
                  chart: { type: "pie" }, 
                  legend: {
                    position: 'bottom',
                    onItemClick: { toggleDataSeries: true } // Allows clicking legend items to hide/show

                  }, 
                  labels: pieChartData.labels,
                  states: {
                    active: {
                      filter: {
                        type: "none", // Disable automatic highlighting
                      }
                    }
                  } 
              }}
                series={pieChartData.values}
                type="pie"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "auto" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Website Views</Typography>
              <ReactApexChart
                options={{
                  chart: { type: "bar" },
                  xaxis: { categories: barChartData.labels },  // Labels for X-axis
                  legend: { position: "bottom" },
                  dataLabels: { enabled: false } // Hides numbers on bars

                }}
                series={[
                  {
                    name: "Bar Chart Data", 
                    data: barChartData.values  // Values for Y-axis
                  }
                ]}
                type="bar"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "auto" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Daily Sales</Typography>
              <ReactApexChart
                options={{
                  chart: { type: "line" },
                  xaxis: { categories: lineChartData.labels }, // X-axis Years
                  legend: { position: "bottom" },
                  stroke: { width: 2 },
                  dataLabels: { enabled: false } // Hide numbers on points
                }}
                series={lineChartData.series} // Two data series: Revenues & Expenses
                type="line"
              />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6} lg={4}>
          <Card sx={{
              height: { xs: "auto", lg: "auto" }, // Auto height on small screens, fixed on large screens
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
              height: { xs: "auto", lg: "auto" }, // Auto height on small screens, fixed on large screens
            }}>
            <CardContent>
              <Typography variant="h6">Daily Sales</Typography>
              <ReactApexChart
                options={{
                  chart: { type: "bar" },
                  xaxis: { categories: netBarChartData.labels },  // Labels for X-axis
                  legend: { position: "bottom" },
                  dataLabels: { enabled: false } // Hides numbers on bars

                }}
                series={[
                  {
                    name: "Bar Chart Data", 
                    data: netBarChartData.values  // Values for Y-axis
                  }
                ]}
                type="bar"
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
