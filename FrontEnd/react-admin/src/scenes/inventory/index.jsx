import React from "react";
import { Box, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockInventory } from "../../data/mockData";
import Header from "../../components/Header";

const Team = () => {
  // Access theme and colors
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // Define column configuration
  const columns = [
    { field: "id", headerName: "ID" },
    { field: "item", headerName: "Item", flex: 1, cellClassName: "name-column--cell" },
    { field: "quantity", headerName: "Quantity", type: "number", flex: 1, headerAlign: "left", align: "left" },
    { field: "idealQuantity", headerName: "Ideal Quantity", flex: 1, headerAlign: "left", align: "left" },
  ];

  return (
    <Box m="20px">
      {/* Header */}
      <Header title="Inventory" subtitle="List of company property" />

      {/* DataGrid container */}
      <Box m="40px 0 0 0" height="75vh">
        {/* DataGrid component */}
        <DataGrid
          checkboxSelection
          rows={mockInventory}
          columns={columns}
          // Custom styling
          sx={{
            "& .MuiDataGrid-root": { border: "none" },
            "& .MuiDataGrid-cell": { borderBottom: "none" },
            "& .name-column--cell": { color: colors.greenAccent[300] },
            "& .MuiDataGrid-columnHeaders": { backgroundColor: colors.blueAccent[700], borderBottom: "none" },
            "& .MuiDataGrid-virtualScroller": { backgroundColor: colors.primary[400] },
            "& .MuiDataGrid-footerContainer": { borderTop: "none", backgroundColor: colors.blueAccent[700] },
            "& .MuiCheckbox-root": { color: `${colors.greenAccent[200]} !important` },
          }}
        />
      </Box>
    </Box>
  );
};

export default Team;
