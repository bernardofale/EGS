import React, { useState } from "react";
import { Box, useTheme,Typography } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import { tokens } from "../../theme";

const Noti = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  // Dados das notificações com classificação de prioridade
  const [notifications] = useState([
    { id: 1, title: "Acabar de alterar o template", content: "Personalização total ao projeto" },
    { id: 2, title: "Adaptar para receber dados das api", content: "Use_effects e fetch" },
    { id: 3, title: "Tratar da autenticação", content: "Diferenciar o login por role" }
  ]);


  return (
    <Box m="20px">
      <Header title="Notifications" />

      {notifications.map((notification, index) => (
        <Accordion key={index} defaultExpanded>
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
