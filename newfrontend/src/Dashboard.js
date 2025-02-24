import React, { useEffect, useState } from "react";
import { Grid, Card, CardContent, Typography, Box, Paper } from "@mui/material";
import ReactApexChart from "react-apexcharts";
import Navbar from "./components/Navbar";
import { fetchPieChartData } from "./service/api1";
import { fetchBarChartData } from "./service/api2";
import { fetchLineChartData } from "./service/api3";
import { fetchNetBarChartData } from "./service/api5";
import { fetchFundTableData } from "./service/api4";
import FundTableComponent from "./components/FundTableComponent";
import Security from "./components/Security";



function Dashboard() {
  const [filters, setFilters] = useState({ department: "", start_date: "", end_date: "" });
  const [pieChartData, setPieChartData] = useState({ labels: [], values: [] });
  const [barChartData, setBarChartData] = useState({ labels: [], values: [] });
  const [lineChartData, setLineChartData] = useState({ labels: [], series: [] });
  const [netBarChartData, setnetBarChartData] = useState({ labels: [], series: [] });
  const [fundTableData, setFundTableData] = useState([]);


  useEffect(() => {
    async function getData() {
      const piePromise = fetchPieChartData(filters);
      const barPromise = fetchBarChartData(filters);
      const linePromise = fetchLineChartData(filters);
      const netBarPromise = fetchNetBarChartData(filters);
      const fundTablePromise = fetchFundTableData(filters);

      // Wait for all promises to resolve (they run simultaneously)
      const [pieData, barData, lineData, netBarData, fundTableData] = await Promise.all([piePromise, barPromise, linePromise, netBarPromise, fundTablePromise]);

      
      setPieChartData({ labels: pieData.labels, values: pieData.values });
      setBarChartData({ labels: barData.labels, values: barData.values });
      setLineChartData({
        labels: lineData.years, // X-axis (Years)
        series: [
            { name: "Revenues", data: lineData.revenues },
            { name: "Expenses", data: lineData.expenses }
        ]
      });
      setnetBarChartData({ labels: netBarData.times, values: netBarData.net_profits })
      setFundTableData(fundTableData);

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

  const formatNumber = (num) => {
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1) + 'B'; // Converts large numbers to "B" for billions
  } else if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'; // Converts numbers in millions to "M"
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'; // Converts numbers in thousands to "K"
  }
  return num.toLocaleString(); // Add commas for smaller numbers
};

    return (
      <>
      <Security />
        <Navbar onFilterChange={handleFilterChange} />
        <Box p={3} mt={10} sx={{ minHeight: "100vh", backgroundColor: "#f5f5f5", display: "flex", flexDirection: "column" }}>
          <Grid container spacing={3} sx={{ flexGrow: 1 }}>
          
            {/* Department Budget Breakdown */}
            <Grid item xs={12} md={8} lg={8}>
              <Paper sx={{ display: 'flex', flexDirection: 'column', height: '100%', boxShadow: 3, borderRadius: 3 }}>
                <CardContent sx={{ padding: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: "#333" }}>
                    Department Budget Breakdown
                  </Typography>
                  <ReactApexChart
                    options={{
                      chart: {
                        type: "bar",
                        width: '100%',
                        toolbar: { show: true }
                      },
                      xaxis: {
                        categories: barChartData.labels,
                        labels: {
                          style: { fontSize: '10px' }
                        }
                      },
                      legend: { position: "bottom" },
                      dataLabels: {
                        enabled: true,
                        formatter: function (val) {
                          return formatNumber(val); 
                        },
                        style: {
                          fontSize: '12px',  
                          colors: ['#000'],  
                        },
                        offsetX: 80, 
                        position: 'top',  
                      },
                      plotOptions: {
                        bar: { 
                          horizontal: true, 
                        }
                      },
                      colors: ['#3357FF'],
                      toolbar: { show: true }
                    }}
                    series={[{ name: "Bar Chart Data", data: barChartData.values }]}
                    type="bar"
                    height={400}
                    width="100%"
                  />
                </CardContent>
              </Paper>
            </Grid>
            
  
            {/* Top ROI Sources */}
            <Grid item xs={12} md={4} lg={4}>
              <Paper sx={{ display: 'flex', flexDirection: 'column', height: '100%', boxShadow: 3, borderRadius: 3 }}>
                <CardContent sx={{ padding: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: "#333" }}>
                    Top ROI Sources
                  </Typography>
                  <ReactApexChart
                    options={{
                      chart: { type: "pie", width: '100%' },
                      legend: { position: 'bottom', onItemClick: { toggleDataSeries: true } },
                      labels: pieChartData.labels,
                      states: { active: { filter: { type: "none" } } },
                      dataLabels: { enabled: true },
                      stroke: { width: 0 },
                      colors: ['#FF5733', '#33FF57', '#3357FF', '#FF33A6', '#33A6FF', '#A6FF33', '#A633FF', '#FF8C33']
                    }}
                    series={pieChartData.values}
                    type="pie"
                    height={400}
                    width="100%"
                  />
                </CardContent>
              </Paper>
            </Grid>
  
            {/* Revenue vs Expenses */}
            <Grid item xs={12} md={6} lg={6}>
              <Paper sx={{ display: 'flex', flexDirection: 'column', height: '100%', boxShadow: 3, borderRadius: 3 }}>
                <CardContent sx={{ padding: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: "#333" }}>
                    Revenue vs Expenses
                  </Typography>
                  <ReactApexChart
                    options={{
                      chart: { type: "line", width: '100%' },
                      xaxis: {
                        categories: lineChartData.labels,
                        labels: { style: { fontSize: '10px' } }
                      },
                      legend: { position: "bottom" },
                      stroke: { width: 5 },
                      dataLabels: {
                        enabled: true,
                        formatter: function (val) {
                          return formatNumber(val); // Apply formatting to data labels
                        }
                      },
                      grid: { borderColor: '#e5e5e5' }
                    }}
                    series={lineChartData.series}
                    type="line"
                    height={300}
                    width="100%"
                  />
                </CardContent>
              </Paper>
            </Grid>
  
            {/* Net Profit */}
            <Grid item xs={12} md={6} lg={6}>
              <Paper sx={{ display: 'flex', flexDirection: 'column', height: '100%', boxShadow: 3, borderRadius: 3 }}>
                <CardContent sx={{ padding: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: "#333" }}>
                    Net Profit
                  </Typography>
                  <ReactApexChart
                    options={{
                      chart: { type: "bar", width: '100%' },
                      xaxis: {
                        categories: netBarChartData.labels,
                        labels: { style: { fontSize: '10px' } }
                      },
                      legend: { position: "bottom" },
                      dataLabels: {
                        enabled: true,
                        formatter: function (val) {
                          return formatNumber(val); // Apply formatting to data labels
                        }
                      },
                      grid: { borderColor: '#e5e5e5' },
                      colors: ['#00FF7F']
                    }}
                    series={[{ name: "Net Data", data: netBarChartData.values }]}
                    type="bar"
                    height={300}
                    width="100%"
                  />
                </CardContent>
              </Paper>
            </Grid>
  
            {/* Fund Performance */}
            <Grid item xs={12}>
              <Paper sx={{ display: 'flex', flexDirection: 'column', height: 'auto', boxShadow: 3, borderRadius: 3 }}>
                <CardContent sx={{ padding: 3 }}>
                  <Typography variant="h6" gutterBottom sx={{ fontWeight: 600, color: "#333" }}>
                    Fund Performance
                  </Typography>
                  <FundTableComponent data={fundTableData} />
                </CardContent>
              </Paper>
            </Grid>
  
          </Grid>
        </Box>
      </>
    );
  };
  
  export default Dashboard;