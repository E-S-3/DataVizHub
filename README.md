<h1 align="center" id="title">DataVizHub</h1>

<p id="description">DataVizHub is a modern financial dashboard designed to manage visualize and analyze large-scale financial data. It provides a seamless experience by integrating a high-performance backend powered by FastAPI an interactive ReactJS frontend and a robust MySQL database. The system enables real-time financial insights with intuitive visualizations and efficient data processing.</p>

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   Real-Time Data Visualization: Interactive charts (Pie Bar Line) for ROI budget expenditure revenue expenses and net profit.
*   High-Performance Backend: FastAPI with asynchronous capabilities to handle large data volumes efficiently.
*   Modular Frontend: ReactJS with optimized UI using React Hooks and Context API.
*   Scalable Database: MySQL for efficient storage retrieval and transaction handling.
*   API Performance Monitoring: Middleware tracks API response times logging speed metrics for analysis.
*   Performance Analysis: A script calculates average max and min response times based on logs.
*   CI/CD Pipeline: GitHub Actions for automated deployment rollback and high availability with Docker and Kubernetes.
*   Authentication and Security: Google Sign-In with Firebase for seamless authentication and session management.

<h2>🛠️ Installation Steps:</h2>

<p>1. Create the MYSQL Database &amp; Run SQL files</p>

```
CREATE DATABASE data_viz_hub;
```

<p>2. Run the SQL Scripts provided SQL in MySQL to initialize tables and insert  data.</p>

<p>3. Clone the Repository</p>

```
git clone https://github.com/SurentharRajamohan/DataVizHub.git cd DataVizHub
```

<p>4. Set Up the Backend (FastAPI)</p>

```
cd backend pip install -r requirements.txt uvicorn app.main:app --reload
```

<p>5. Set Up the Frontend (ReactJS)</p>

```
cd frontend npm install npm start
```

<p>6. Run the Performance Analysis</p>

```
python performance_analysis.py
```

<p>7. API Tests</p>

```
pytest tests/test_api.py
```

<p>8. Query Tests</p>

```
pytest tests/test_queries.py
```

<p>9. Stress Test</p>

```
locust
```

  
  
<h2>💻 Built with</h2>

Technologies used in the project:

*   FastAPI
*   ReactJS
*   MySQL
*   GitHub Actions with Docker
*   Kubernetes (Minikube for local testing)
*   Firebase Google Sign-In
*   Pandas
