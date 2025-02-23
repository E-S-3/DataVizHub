export async function fetchLineChartData(filters) {
    const baseUrl = "http://127.0.0.1:8000/api/revenue-expenses/";
    
    // Remove empty filter values
    const filteredParams = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value)
    );

    const queryParams = new URLSearchParams(filteredParams).toString();
    const url = queryParams ? `${baseUrl}?${queryParams}` : baseUrl;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        console.log("Response:", response);
        return await response.json();
    } catch (error) {
        console.error("Error fetching pie chart data:", error);
        return { labels: [], values: [] };
    }
}
