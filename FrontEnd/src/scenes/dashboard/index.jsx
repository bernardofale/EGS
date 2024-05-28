import { Box, Typography, useTheme } from "@mui/material";
import axios from 'axios';
import Cookies from 'js-cookie';
import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const getMostRecentDocument = (documents) => {
  return documents.reduce((latest, current) => {
    return new Date(current.date) > new Date(latest.date) ? current : latest;
  }, documents[0]);
};

const getMostRecentTask = (tasks) => {
  return tasks.reduce((latest, current) => {
    return new Date(current.due_date) > new Date(latest.due_date) ? current : latest;
  }, tasks[0]);
};

const getMostRecentMeeting = (meetings) => {
  return meetings.reduce((earliest, current) => {
    return new Date(current.start_date) < new Date(earliest.start_date) ? current : earliest;
  }, meetings[0]);
};

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const documents = JSON.parse(process.env.REACT_APP_DOCUMENTS);
  const mostRecentDocument = getMostRecentDocument(documents);
  const truncatedContent =
    mostRecentDocument.content.length > 200
      ? `${mostRecentDocument.content.slice(0, 200)}...`
      : mostRecentDocument.content;

  const [mostRecentTask, setMostRecentTask] = useState(null);
  const [mostRecentMeeting, setMostRecentMeeting] = useState(null);

  useEffect(() => {
    const token = Cookies.get('access_token');

    const fetchTodo = async () => {
      try {
        const response = await axios.get('/todos', {
          headers: {
            'accept': 'application/json'
          },
          params: {
            token: token
          }
        });
        if (response.data && typeof response.data === 'object') {
          const todoArray = Object.values(response.data);
          setMostRecentTask(getMostRecentTask(todoArray));
        } else {
          console.error("Erro: Dados recebidos não são um objeto esperado");
          setMostRecentTask(null);
        }
      } catch (error) {
        console.error("Erro ao buscar as tarefas:", error);
        setMostRecentTask(null);
      }
    };

    const fetchMeetings = async () => {
      try {
        const response = await axios.get('/meetings', {
          headers: {
            'accept': 'application/json'
          },
          params: {
            token: token
          }
        });
        if (response.data && typeof response.data === 'object') {
          const meetingsArray = Object.values(response.data); // Extrai os valores do objeto
          setMostRecentMeeting(getMostRecentMeeting(meetingsArray));
        } else {
          console.error("Erro: Dados recebidos não são um objeto esperado");
          setMostRecentMeeting(null);
        }
      } catch (error) {
        console.error("Erro ao buscar as reuniões:", error);
        setMostRecentMeeting(null);
      }
    };

    fetchTodo();
    fetchMeetings();
  }, []);

  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
      </Box>

      <Box
        display="grid"
        gridTemplateColumns="repeat(10, 1fr)"
        gridAutoRows="140px"
        gap="20px"
      >
        {/* New Document Box with Preview */}
        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="space-between"
          borderRadius="15px"
          p={4}
          textAlign="center"
        >
          {/* Title */}
          <Typography variant="h2" color="textSecondary" gutterBottom>
            {mostRecentDocument.name}
          </Typography>
          {/* Description */}
          <Typography variant="h4" color="textSecondary" gutterBottom>
            {mostRecentDocument.description}
          </Typography>
          {/* Content (truncated) */}
          <Typography variant="h5" color="textSecondary" gutterBottom>
            {truncatedContent}
          </Typography>
          {/* Date */}
          <Typography variant="h5" color="textSecondary">
            {new Date(mostRecentDocument.date).toLocaleDateString()}
          </Typography>
        </Box>

        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px"
          textAlign="center"
          p={4}
        >
          <Typography variant="h3" color="textPrimary" gutterBottom>
            Earliest meeting
          </Typography>
          {mostRecentMeeting ? (
            <>
              <Typography variant="h4" color="textSecondary" gutterBottom>
                Meeting: {mostRecentMeeting.title}
              </Typography>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                Date: {new Date(mostRecentMeeting.start_date).toLocaleDateString()}
              </Typography>
              <Typography variant="h6" color="textSecondary">
                Location: {mostRecentMeeting.location}
              </Typography>
              <Typography variant="h6" color="textSecondary">
                Attendee: {mostRecentMeeting.created_by}
              </Typography>
            </>
          ) : (
            <Typography variant="h4" color="textSecondary">
              No meetings available
            </Typography>
          )}
        </Box>
        
        {/* Box 3 */}
        <Box
          gridColumn="span 3"
          gridRow="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
          borderRadius="15px"
          textAlign="center"
        >
          {mostRecentTask ? (
            <Box textAlign="center">
              <Typography variant="h3" color="textPrimary" gutterBottom>
                Task with the earliest due date
              </Typography>
              <Typography variant="h4" color="textSecondary" gutterBottom>
                Task: {mostRecentTask.description}
              </Typography>
              <Typography variant="h5" color="textSecondary" gutterBottom>
                Description: {mostRecentTask.content}
              </Typography>
              <Typography variant="h6" color="textSecondary">
                Due Date: {new Date(mostRecentTask.due_date).toLocaleDateString()}
              </Typography>
            </Box>
          ) : (
            <Typography variant="h4" color="textSecondary">
              No tasks available
            </Typography>
          )}
        </Box>
      
      </Box>
    </Box>
  );
};

export default Dashboard;
