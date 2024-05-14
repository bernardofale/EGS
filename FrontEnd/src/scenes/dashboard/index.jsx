import React from "react";
import { Typography } from "@mui/material";
import { Box, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(10, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        
        {/* Box 1 */}
        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px" 
        >
          <Typography variant="h3" color="textPrimary" gutterBottom>
            New Document
          </Typography>
        </Box>

        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px" 
        >
          <Typography variant="h3" color="textPrimary" gutterBottom>
            Meetings
          </Typography>
        </Box>
        
        {/* Box 2 */}
        <Box
          gridColumn="span 4"
          gridRow="span 2"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px" 
        >
          <Typography variant="h3" color="textPrimary" gutterBottom>
            Most recent notifications
          </Typography>
        </Box>
        
        {/* Box 3 */}
        <Box
          gridColumn="span 4"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px" 
        >
          <Typography variant="h3" color="textPrimary" gutterBottom>
            Most priority task
          </Typography>
        </Box>
      
      </Box>
    </Box>
  );
};

export default Dashboard;
