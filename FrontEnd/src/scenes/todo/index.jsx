import DeleteIcon from '@mui/icons-material/Delete';
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import StarIcon from "@mui/icons-material/Star";
import StarBorderIcon from "@mui/icons-material/StarBorder";
import { Accordion, AccordionDetails, AccordionSummary, Box, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Grid, TextField, Typography, useTheme } from "@mui/material";
import axios from 'axios';
import Cookies from 'js-cookie';
import React, { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const ToDo = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [todo, setTodo] = useState([]);
  const [open, setOpen] = useState(false);
  const [newTask, setNewTask] = useState({
    description: '',
    completed: false,
    priority: 1,
    meeting_id: '',
    content: '',
    departamento_id: 0,
    due_date: ''
  });

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
          setTodo(todoArray);
        } else {
          console.error("Erro: Dados recebidos não são um objeto esperado");
          setTodo([]);
        }
      } catch (error) {
        console.error("Erro ao buscar as tarefas:", error);
        setTodo([]);
      }
    };

    fetchTodo();

    const interval = setInterval(fetchTodo, 5000); // Atualiza a cada 5 segundos

    return () => clearInterval(interval); // Limpa o intervalo quando o componente é desmontado
  }, []);

  const sortTodoByPriority = () => {
    const sortedTodo = [...todo];
    sortedTodo.sort((a, b) => b.priority - a.priority);
    setTodo(sortedTodo);
  };

  const sortTodoByName = () => {
    const sortedTodo = [...todo];
    sortedTodo.sort((a, b) => a.description.localeCompare(b.description));
    setTodo(sortedTodo);
  };

  const handleDeleteTask = async (taskId) => {
    const token = Cookies.get('access_token');
    try {
      await axios.delete(`/todos/${taskId}`, {
        headers: {
          'accept': 'application/json'
        },
        params: {
          token: token
        }
      });
      const updatedTodo = todo.filter(task => task.id !== taskId);
      setTodo(updatedTodo);
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error);
    }
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

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    setNewTask(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleAddTask = async () => {
    const token = Cookies.get('access_token');
    try {
      const response = await axios.post('/todos', newTask, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
        params: {
          token: token
        }
      });
      if (response.data) {
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
              setTodo(todoArray);
            } else {
              console.error("Erro: Dados recebidos não são um objeto esperado");
              setTodo([]);
            }
          } catch (error) {
            console.error("Erro ao buscar as tarefas:", error);
            setTodo([]);
          }
        };

        fetchTodo(); // Chama a função fetchTodo para atualizar a lista
        handleClose();
      }
    } catch (error) {
      console.error("Erro ao adicionar a tarefa:", error);
    }
  };

  return (
    <Box m="20px">
      <Header title="To Do List" subtitle="A list of the company tasks"/>

      <Box display="flex" justifyContent="center" mb={2}>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }} onClick={handleClickOpen}>Add Task</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', marginRight: '8px', opacity: 0.8 }} onClick={sortTodoByPriority}>Sort by Priority</Button>
        <Button variant="contained" color="primary" style={{ border: '1px solid white', opacity: 0.8 }} onClick={sortTodoByName}>Sort by Title</Button>
      </Box>

      {todo.map((task) => (
        <Accordion key={task.id} defaultExpanded>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            <Box display="flex" alignItems="center" justifyContent="space-between" width="100%">
              <Typography color={colors.greenAccent[500]} variant="h5">
                {task.description}
              </Typography>
              <Box ml={2} display="flex" alignItems="center">
                {renderPriorityStars(task.priority)}
                <Button variant="contained" color="secondary" onClick={() => handleDeleteTask(task.id)} startIcon={<DeleteIcon />} style={{ marginLeft: '8px' }}>Delete</Button>
              </Box>
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>
              {task.content}
            </Typography>
          </AccordionDetails>
        </Accordion>
      ))}

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Add New Task</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please fill out the form below to add a new task.
          </DialogContentText>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                autoFocus
                margin="dense"
                name="description"
                label="Description"
                type="text"
                fullWidth
                value={newTask.description}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                margin="dense"
                name="content"
                label="Content"
                type="text"
                fullWidth
                value={newTask.content}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                margin="dense"
                name="priority"
                label="Priority"
                type="number"
                fullWidth
                value={newTask.priority}
                onChange={handleChange}
                variant="outlined"
                inputProps={{ min: "1", max: "5", step: "1" }}
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                margin="dense"
                name="meeting_id"
                label="Meeting ID"
                type="text"
                fullWidth
                value={newTask.meeting_id}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                margin="dense"
                name="departamento_id"
                label="Department ID"
                type="number"
                fullWidth
                value={newTask.departamento_id}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={6}>
              <TextField
                margin="dense"
                name="due_date"
                label="Due Date"
                type="datetime-local"
                fullWidth
                InputLabelProps={{
                  shrink: true,
                }}
                value={newTask.due_date}
                onChange={handleChange}
                variant="outlined"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
          <Button onClick={handleAddTask} color="primary">
            Add Task
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ToDo;
