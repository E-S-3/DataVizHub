export async function initialise() {
    const baseUrl = "http://127.0.0.1:8000/api/initialise/";
    
    try {
        const response = await fetch(baseUrl);
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching pie chart data:", error);
        return { departments: [
            {
              "id": 101,
              "name": "City Council"
            },
            {
              "id": 102,
              "name": "Mayor's Office"
            },
            {
              "id": 103,
              "name": "Innovation and Performance"
            },
            {
              "id": 105,
              "name": "Human Relations Commission"
            },
            {
              "id": 106,
              "name": "Controller's Office"
            },
            {
              "id": 107,
              "name": "Department of Finance"
            },
            {
              "id": 108,
              "name": "Department of Law"
            },
            {
              "id": 109,
              "name": "Personnel/Civil Service"
            },
            {
              "id": 110,
              "name": "Department of City Planning"
            },
            {
              "id": 112,
              "name": "City Clerk"
            },
            {
              "id": 121,
              "name": "Finance, Procurement and Fleet"
            },
            {
              "id": 122,
              "name": "Office of Management and Budget"
            },
            {
              "id": 130,
              "name": "Permits Licenses and Inspection"
            },
            {
              "id": 183,
              "name": "Equal Opportunity Review Committee"
            },
            {
              "id": 210,
              "name": "Department of Public Safety - Administration"
            },
            {
              "id": 220,
              "name": "Department of Public Safety - Emergency Medical Services"
            },
            {
              "id": 230,
              "name": "Department of Public Safety - Police"
            },
            {
              "id": 240,
              "name": "Office of Municipal Investigations"
            },
            {
              "id": 250,
              "name": "Department of Public Safety - Fire"
            },
            {
              "id": 270,
              "name": "Department of Public Safety - Building Inspection"
            },
            {
              "id": 280,
              "name": "Department of Public Safety - Animal Care and Control"
            },
            {
              "id": 400,
              "name": "Public Works"
            },
            {
              "id": 410,
              "name": "Department of Public Works - Administration"
            },
            {
              "id": 420,
              "name": "Department of Public Works - Operations"
            },
            {
              "id": 430,
              "name": "Department of Public Works - Environmental Services"
            },
            {
              "id": 440,
              "name": "Department of Public Works - Transportation and Engine"
            },
            {
              "id": 450,
              "name": "Department of Public Works - Facilities"
            },
            {
              "id": 500,
              "name": "Parks and Recreation"
            },
            {
              "id": 600,
              "name": "Mobility and Infrastructure"
            },
            {
              "id": 820,
              "name": "Urban Redevelopment Authority Projects"
            },
            {
              "id": 840,
              "name": "Equipment Leasing Authority"
            }
          ], earliest_date: "2012-01-03", latest_date: "2020-12-31" };
    }
}
