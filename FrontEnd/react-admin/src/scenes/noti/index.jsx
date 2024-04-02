import React, { useState } from "react";
import { Box, useTheme, Button, Typography } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import StarIcon from "@mui/icons-material/Star";
import StarBorderIcon from "@mui/icons-material/StarBorder";
import { tokens } from "../../theme";

const Noti = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // Dados das notificações com classificação de prioridade
  const [notifications, setNotifications] = useState([
    { id: 1, priority: 3, title: "Acabar de alterar o template", content: "Personalização total ao projeto" },
    { id: 2, priority: 2, title: "Adaptar para receber dados das api", content: "Use_effects e fetch" },
    { id: 3, priority: 4, title: "Tratar da autenticação", content: "Diferenciar o login por role" }
  ]);

  // Função para classificar as notificações por prioridade
  const sortNotificationsByPriority = () => {
    const sortedNotifications = [...notifications];
    sortedNotifications.sort((a, b) => b.priority - a.priority); // Ordena de forma decrescente pela prioridade
    setNotifications(sortedNotifications);
  };

  // Função para classificar as notificações por ordem alfabética do título
  const sortNotificationsByName = () => {
    const sortedNotifications = [...notifications];
    sortedNotifications.sort((a, b) => a.title.localeCompare(b.title)); // Ordena em ordem alfabética pelo título
    setNotifications(sortedNotifications);
  };


  const renderPriorityStars = (priority) => {
    const stars = [];
    const starColor = "#FFD700"; // Cor amarela para as estrelas
    const emptyStarColor = "#9E9E9E"; // Cor cinza para as estrelas vazias
    for (let i = 1; i <= 5; i++) {
      if (i <= priority) {
        stars.push(<StarIcon key={i} style={{ color: starColor, marginRight: '2px' }} />);
      } else {
        stars.push(<StarBorderIcon key={i} style={{ color: emptyStarColor, marginRight: '2px' }} />);
      }
    }
    return stars;
  };

  return (
    <Box m="20px">
      <Header title="Notifications" />

      <Box display="flex" justifyContent="center" mb={2}>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }}>Add Notification</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }} onClick={sortNotificationsByPriority}>Sort by Priority</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', opacity: 0.8 }} onClick={sortNotificationsByName}>Sort by Name</Button>
      </Box>

      {notifications.map((notification, index) => (
        <Accordion key={index} defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
              <Typography color={colors.greenAccent[500]} variant="h5">
                {notification.title}
              </Typography>
              <Box ml={2} display="flex" alignItems="center">
                {renderPriorityStars(notification.priority)}
              </Box>
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
