import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { Box, Typography, useTheme } from "@mui/material";
import Accordion from "@mui/material/Accordion";
import AccordionDetails from "@mui/material/AccordionDetails";
import AccordionSummary from "@mui/material/AccordionSummary";
import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const Noti = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const data = JSON.parse(process.env.REACT_APP_NOTIFICATIONS);
        setNotifications(data);
      } catch (error) {
        console.error("Erro ao buscar notificações:", error);
      }
    };

    fetchNotifications();
  }, []);

  return (
    <Box m="20px">
      <Header title="Notifications" />

      {notifications.map((notification) => (
        <Accordion key={notification.id} defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
              <Typography color={colors.greenAccent[500]} variant="h5">
                {notification.title}
              </Typography>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              {notification.content}
            </Typography>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

export default Noti;
