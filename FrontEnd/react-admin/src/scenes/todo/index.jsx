import React, { useState } from "react";
import { Box, useTheme, Button, Typography, Chip } from "@mui/material";
import Header from "../../components/Header";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import StarIcon from "@mui/icons-material/Star";
import StarBorderIcon from "@mui/icons-material/StarBorder";
import DoneIcon from '@mui/icons-material/Done';
import UndoIcon from '@mui/icons-material/Undo';
import { tokens } from "../../theme";

const ToDo = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const [todo, settodo] = useState([
    { id: 1, priority: 3, title: "Acabar de alterar o template", content: "Personalização total ao projeto", done: false },
    { id: 2, priority: 2, title: "Adaptar para receber dados das api", content: "Use_effects e fetch", done: false },
    { id: 3, priority: 4, title: "Tratar da autenticação", content: "Diferenciar o login por role", done: false }
  ]);

  const sorttodoByPriority = () => {
    const sortedtodo = [...todo];
    sortedtodo.sort((a, b) => b.priority - a.priority);
    settodo(sortedtodo);
  };

  const sorttodoByName = () => {
    const sortedtodo = [...todo];
    sortedtodo.sort((a, b) => a.title.localeCompare(b.title));
    settodo(sortedtodo);
  };

  const handleTaskDone = (taskId) => {
    const updatedTodo = todo.map(task =>
      task.id === taskId ? { ...task, done: true } : task
    );
    settodo(updatedTodo);
  };

  const handleTaskUndone = (taskId) => {
    const updatedTodo = todo.map(task =>
      task.id === taskId ? { ...task, done: false } : task
    );
    settodo(updatedTodo);
  };

  const renderPriorityStars = (priority) => {
    const stars = [];
    const starColor = "#FFD700";
    const emptyStarColor = "#9E9E9E";
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
      <Header title="To Do List" subtitle="A list of the company tasks"/>

      <Box display="flex" justifyContent="center" mb={2}>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }}>Add Task</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }} onClick={sorttodoByPriority}>Sort by Priority</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', opacity: 0.8 }} onClick={sorttodoByName}>Sort by Name</Button>
      </Box>

      {todo.map((task, index) => (
        <Accordion key={index} defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
              <Typography color={colors.greenAccent[500]} variant="h5">
                {task.title}
              </Typography>
              <Box ml={2} display="flex" alignItems="center">
                {renderPriorityStars(task.priority)}
                {!task.done && (
                  <Button variant="contained" color="secondary" onClick={() => handleTaskDone(task.id)} style={{ marginLeft: '8px' }}>Done</Button>
                )}
                {task.done && (
                  <Button variant="contained" color="primary" onClick={() => handleTaskUndone(task.id)} startIcon={<UndoIcon />} style={{ marginLeft: '8px' }}></Button>
                )}
              </Box>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              {task.content}
            </Typography>
            {task.done && <Chip icon={<DoneIcon />} label="Done" color="primary" />}
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
};

export default ToDo;
