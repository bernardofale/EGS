import { Box, IconButton, useTheme, Dialog, DialogTitle, DialogContent, DialogActions, Button } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { tokens } from "../../theme";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";

const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const navigate = useNavigate();
  const [isLeaveDialogOpen, setLeaveDialogOpen] = useState(false);


  const handleNotificationsClick = () => {
    navigate("/noti");
  };

  const handlePersonClick = () => {
    setLeaveDialogOpen(true);
  };

  const handleLeaveConfirmation = () => {
    navigate("/login");
    setLeaveDialogOpen(false);
  };

  const handleCloseLeaveDialog = () => {
    setLeaveDialogOpen(false);
  };

  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      {/* SEARCH BAR */}
      <Box
        display="flex"
        backgroundColor={colors.primary[400]}
        borderRadius="3px"
      >
      </Box>

      {/* ICONS */}
      <Box display="flex">

        <IconButton onClick={handleNotificationsClick}>
          <NotificationsOutlinedIcon />
        </IconButton>

        <IconButton onClick={handlePersonClick}>
          <PersonOutlinedIcon />
        </IconButton>
      </Box>

      {/* LEAVE CONFIRMATION DIALOG */}
      <Dialog open={isLeaveDialogOpen} onClose={handleCloseLeaveDialog}>
        <DialogTitle>Confirmation</DialogTitle>
        <DialogContent>
          Are you sure you want to leave?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleLeaveConfirmation} variant="contained" color="primary">
            Yes
          </Button>
          <Button onClick={handleCloseLeaveDialog} color="secondary">
            No
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Topbar;
