import DescriptionOutlinedIcon from "@mui/icons-material/DescriptionOutlined";
import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import React, { useState } from "react";
import DocumentModal from "../../components/DocumentModal"; // Ensure this is the correct path
import Header from "../../components/Header";
import { tokens } from "../../theme";

const Documents = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [open, setOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState(null);

  const documents = JSON.parse(process.env.REACT_APP_DOCUMENTS);

  const handleRowClick = (params) => {
    setSelectedDocument(params.row);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setSelectedDocument(null);
  };

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
    <Box m="10px">
      <Header title="Documents" subtitle="Browse and manage company documents" />
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
        <DataGrid
          rows={documents}
          columns={columns}
          onRowClick={handleRowClick}
        />
      </Box>
      {selectedDocument && (
        <DocumentModal
          open={open}
          onClose={handleClose}
          document={selectedDocument}
        />
      )}
    </Box>
  );
};

export default Documents;
