import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import FullCalendar from "@fullcalendar/react";
import {
  Box,
  List,
  ListItem,
  ListItemText,
  Typography,
  useTheme,
} from "@mui/material";
import axios from "axios";
import Cookies from "js-cookie";
import { useEffect, useState } from "react";
import Header from "../../components/Header";
import { tokens } from "../../theme";

const formatDate = (date) => {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(date);
};

const Calendar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [currentEvents, setCurrentEvents] = useState([]);

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    const token = Cookies.get('access_token');
    try {
      const response = await axios.get('/meetings', {
        headers: {
          'accept': 'application/json'
        },
        params: {
          token: token
        }
      });
      const meetings = response.data.map(meeting => ({
        id: meeting.id,
        title: meeting.title,
        start: meeting.start_date,
        end: meeting.end_date,
      }));
      setCurrentEvents(meetings);
    } catch (error) {
      console.error("Erro ao buscar reuniões:", error);
    }
  };

  const handleEventClick = async (selected) => {
    const action = prompt("Type 'edit' to edit the meeting or 'delete' to delete it");

    if (action === 'delete') {
      if (window.confirm(`Are you sure you want to delete the event '${selected.event.title}'?`)) {
        const token = Cookies.get('access_token');
        try {
          await axios.delete(`/meetings/${selected.event.id}`, {
            headers: {
              'accept': 'application/json'
            },
            params: {
              token: token
            }
          });
          selected.event.remove();
          fetchMeetings();
        } catch (error) {
          console.error("Erro ao deletar reunião:", error);
        }
      }
    } else if (action === 'edit') {
      const newTitle = prompt("Please enter a new title for your event", selected.event.title);
      if (newTitle) {
        const token = Cookies.get('access_token');
        try {
          await axios.put(`/meetings/${selected.event.id}`, {
            title: newTitle
          }, {
            headers: {
              'accept': 'application/json',
              'Content-Type': 'application/json'
            },
            params: {
              token: token
            }
          });
          selected.event.setProp('title', newTitle);
          fetchMeetings();
        } catch (error) {
          console.error("Erro ao editar reunião:", error);
        }
      }
    }
  };

  return (
    <Box m="20px">
      <Header title="Calendar" />

      <Box display="flex" justifyContent="space-between">
        {/* CALENDAR SIDEBAR */}
        <Box
          flex="1 1 20%"
          backgroundColor={colors.primary[400]}
          p="15px"
          borderRadius="4px"
        >
          <Typography align="center" variant="h5">Events</Typography>
          <List>
            {currentEvents.map((event) => (
              <ListItem
                key={event.id}
                sx={{
                  backgroundColor: colors.greenAccent[500],
                  margin: "10px 0",
                  borderRadius: "2px",
                }}
              >
                <ListItemText
                  primary={event.title}
                  secondary={
                    <Typography>
                      {formatDate(new Date(event.start))}
                    </Typography>
                  }
                />
              </ListItem>
            ))}
          </List>
        </Box>

        {/* CALENDAR */}
        <Box flex="1 1 100%" ml="15px">
          <FullCalendar
            height="75vh"
            plugins={[dayGridPlugin, interactionPlugin]}
            headerToolbar={{
              left: "title",
              center: "",
              right: "prev today next",
            }}
            initialView="dayGridMonth"
            editable={true}
            selectable={true}
            selectMirror={true}
            dayMaxEvents={true}
            eventClick={handleEventClick}
            eventsSet={(events) => setCurrentEvents(events)}
          />
        </Box>
      </Box>
    </Box>
  );
};

export default Calendar;
