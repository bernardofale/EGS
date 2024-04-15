import React from "react";
import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined"; // Ícone para representar documentos
import Header from "../../components/Header";

const Documents = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // Exemplo de dados de documentos
  const documents = [
    { id: 1, name: "Document1.pdf", size: "1.5 MB", type: "PDF", date: "2024-04-15", description: "Lorem ipsum dolor sit amet, consectetur adipiscing elit." },
    { id: 2, name: "Document2.docx", size: "2.1 MB", type: "Word", date: "2024-04-14", description: "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua." },
    { id: 3, name: "Document3.txt", size: "0.3 MB", type: "Text", date: "2024-04-13", description: "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat." },
  ];

  const columns = [
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
      renderCell: ({ row }) => (
        <Box display="flex" alignItems="center">
          <DescriptionOutlinedIcon color="primary" />
          <Typography ml={1}>{row.name}</Typography>
        </Box>
      ),
    },
    {
      field: "size",
      headerName: "Size",
      flex: 1,
    },
    {
      field: "type",
      headerName: "Type",
      flex: 1,
    },
    {
      field: "date",
      headerName: "Date",
      flex: 1,
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1,
    },
  ];

  return (
    <Box m = "10px">
      <Header
        title="Documents"
        subtitle="Browse and manage company documents"
      />
      <Box
        m="10px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid rows={documents} columns={columns} />
      </Box>
    </Box>
  );
};

export default Documents;
