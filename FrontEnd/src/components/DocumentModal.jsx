import { Box, Button, Modal, Typography } from "@mui/material";
import React from "react";

const DocumentModal = ({ open, onClose, document }) => {
  if (!document) return null; // Null check to prevent accessing properties of null document

  return (
    <Modal open={open} onClose={onClose}>
      <Box
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          bgcolor: "background.paper",
          border: "2px solid #000",
          boxShadow: 24,
          p: 4,
          width: 400, // Adjust width as needed
          textAlign: "center",
        }}
      >
        <Typography variant="h4" gutterBottom>
          {document.name}
        </Typography>
        <Typography variant="h6" mb={2}>
          {document.description}
        </Typography>
        <Typography variant="body1" mb={2}>
          {document.content}
        </Typography>
        <Button
          variant="contained"
          color="secondary"
          onClick={onClose}
          sx={{ mt: 2 }}
        >
          Close
        </Button>
      </Box>
    </Modal>
  );
};

export default DocumentModal;
