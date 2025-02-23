export async function fetchFundTableData(filters) {  
    const baseUrl = "http://127.0.0.1:8000/api/fund-table/";
    

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

        const data = await response.json();
        return data.funds || [];  
    } catch (error) {
        console.error("Error fetching table chart data:", error);
        return [];  
    }
}
