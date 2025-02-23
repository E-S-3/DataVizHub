import React from "react";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
  { field: "fund_description", headerName: "Fund Description", flex: 2 },
  { field: "total_revenue", headerName: "Total Revenue", flex: 1, type: "number" },
  { field: "total_expenses", headerName: "Total Expenses", flex: 1, type: "number" },
  { field: "ratio", headerName: "Ratio", flex: 1, type: "number" },
  { field: "roi", headerName: "ROI", flex: 1, type: "number" },
];

const FundTableComponent = ({ data }) => {
  return (
        <DataGrid
          rows={data.map((row, index) => ({ id: index, ...row }))} 
          columns={columns}
          pageSizeOptions={[5, 10, 25]} 
          initialState={{
            pagination: { paginationModel: { pageSize: 5 } }, 
            sorting: { sortModel: [{ field: "total_revenue", sort: "desc" }] }, 
          }}
          disableRowSelectionOnClick 
        />
  );
};

export default FundTableComponent;
