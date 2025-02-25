import re
import pandas as pd

# Define a pattern to match the log lines
log_pattern = r'(\S+) (\S+) (.+?) - (\d+\.\d+) ms'

api_times = {}

# Read the log file
with open('performance.log', 'r') as file:
    for line in file:
        # Use regex to extract the method, URL, and process time
        match = re.match(log_pattern, line.strip())
        if match:
            method = match.group(1)
            url = match.group(3)
            process_time = float(match.group(4))
            
            # Group times by the URL (endpoint) for later averaging
            if url not in api_times:
                api_times[url] = []
            api_times[url].append(process_time)

# Calculate the average response time for each endpoint
data = []
for endpoint, times in api_times.items():
    average_time = sum(times) / len(times)
    max_time = max(times)
    min_time = min(times)
    total_requests = len(times)
    
    data.append([endpoint, average_time, max_time, min_time, total_requests])

# Create a DataFrame to represent the table
df = pd.DataFrame(data, columns=["Endpoint", "Average Time (ms)", "Max Time (ms)", "Min Time (ms)", "Total Requests"])

# Sort the table by average response time
df = df.sort_values(by="Average Time (ms)", ascending=False)

print(df)

df.to_csv("api_performance_report.csv", index=True)
