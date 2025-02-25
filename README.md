# DataVizHub - Financial Microservice Dashboard

Introduction

DataVizHub is a modern financial dashboard designed to manage, visualize, and analyze large-scale financial data. It provides a seamless experience by integrating a high-performance backend powered by FastAPI, an interactive ReactJS frontend, and a robust MySQL database. The system enables real-time financial insights with intuitive visualizations and efficient data processing.

Features

Real-Time Data Visualization: Interactive charts (Pie, Bar, Line) for ROI, budget expenditure, revenue, expenses, and net profit.

High-Performance Backend: FastAPI with asynchronous capabilities to handle large data volumes efficiently.

Modular Frontend: ReactJS with optimized UI using React Hooks and Context API.

Scalable Database: MySQL for efficient storage, retrieval, and transaction handling.

API Performance Monitoring: Middleware tracks API response times, logging speed metrics for analysis.

Performance Analysis: A script calculates average, max, and min response times based on logs.

CI/CD Pipeline: GitHub Actions for automated deployment, rollback, and high availability with Docker and Kubernetes.

Authentication and Security: Google Sign-In with Firebase for seamless authentication and session management.

Load Testing: Locust-based load testing to evaluate API performance under stress conditions.

Tech Stack

Component

Technology Used

Backend

FastAPI

Frontend

ReactJS

Database

MySQL

CI/CD

GitHub Actions with Docker

Containerization

Docker

Orchestration

Kubernetes (Minikube for local testing)

Logging & Performance Monitoring

Python Logging, Pandas

Authentication

Firebase Google Sign-In

Load Testing

Locust

System Architecture

The project follows a Three-Tier Architecture:

Client Browser – ReactJS frontend for user interaction and dynamic visualizations.

Web Server – FastAPI backend for processing data, applying business logic, and exposing API endpoints.

Database Server – MySQL for structured data storage and querying financial records.

API Endpoints

Endpoint

Description

/api/initialise/

Initializes filters for departments and date ranges.

/api/top-roi/

Retrieves top departments with the highest ROI.

/api/top-budget/

Displays the top 10 departments by budget expenditure.

/api/revenue-expenses/

Provides data on revenue and expenses over time.

/api/fund-table/

Displays a detailed fund performance table.

/api/net-profit/

Shows net profit over time.

Database Setup

The project uses MySQL for storing financial data. A pre-configured SQL script is provided to set up the database.

Database Name: data_viz_hubSQL File Location: data_source_cleaning/sql_file/setup.sql

Steps to Set Up the Database:

Create the Database:

CREATE DATABASE data_viz_hub;

Run the SQL ScriptsExecute the provided SQL script in MySQL to initialize tables and insert sample data.

How to Run Locally

Clone the Repository

git clone https://github.com/yourusername/DataVizHub.git
cd DataVizHub

Set Up the Backend (FastAPI)

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Set Up the Frontend (ReactJS)

cd frontend
npm install
npm start

Database Setup (MySQL)

Ensure a running MySQL instance.

Create the data_viz_hub database as per the setup instructions.

The backend connects to MySQL using credentials specified in the configuration file.

Authentication and Security

Google Authentication Sign-In Setup

Firebase Google Sign-In was implemented for secure authentication. Users log in using their Google accounts via Firebase Authentication.

The authentication flow begins when a user clicks the Sign in with Google button.

Firebase's signInWithPopup() triggers a Google authentication prompt.

Upon successful login, Firebase returns an ID token, which is sent to the backend for validation.

If validated, the user is redirected to the dashboard, and authentication persists using Firebase’s onAuthStateChanged().

A Logout button in the navbar calls Firebase’s signOut() function, clearing session data and redirecting users to the login page.



API Performance Monitoring

To ensure fast and efficient API performance, DataVizHub includes a middleware-based logging system and a performance analysis script:

Middleware for Logging API Response Times

Located in middleware.py, this middleware:

Tracks API response times and logs them to performance.log.

Adds an API-Process-Time header in each response.

Performance Analysis Script

Located in performance_analysis.py, this script:

Parses performance.log to extract API response times.

Calculates average, max, and min response times per API.

Generates an API performance report (CSV).

How to Run the Performance Analysis

python performance_analysis.py

This generates api_performance_report.csv, providing insights into API efficiency.

Load Testing with Locust

To evaluate API performance under high-load conditions, we implemented load testing using Locust.

Locust Setup & Execution

Install Locust

pip install locust

Run Locust Load Test

locust -f locustfile.py --host=http://localhost:8000

Access Locust Web UI

Open http://localhost:8089/ in a browser.

Configure user count and spawn rate to simulate concurrent requests.

View real-time performance metrics such as response times and failure rates.

Locust allows us to analyze the API’s handling of concurrent users and identify bottlenecks for optimization.

Deployment

DataVizHub utilizes GitHub Actions and Docker for automated deployment. The pipeline includes:

Build and Push Docker Images

Backend, frontend, and MySQL containers are built and pushed to Docker Hub.

Deployment via Kubernetes

The system is deployed to a Kubernetes cluster (Minikube for local testing).

Rollback (Failure Handling)

The CI/CD pipeline includes a rollback mechanism to restore the last stable deployment.

Running Tests

API Tests

pytest tests/test_api.py

Query Tests

pytest tests/test_queries.py

