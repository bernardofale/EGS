import { Box, Button, Grid, TextField } from "@mui/material";
import axios from 'axios';
import Cookies from 'js-cookie';
import React, { useState } from "react";
import Header from "../../components/Header";

const Meetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [meetingTitle, setMeetingTitle] = useState("");
  const [location, setLocation] = useState("");
  const [attendee, setAttendee] = useState({ user_id: "", status: "pending" });
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const addMeeting = async () => {
    const token = Cookies.get('token');

    if (!meetingTitle || !location || !startDate || !endDate || !attendee.user_id) {
      console.error("Preencha todos os campos obrigatórios.");
      return;
    }

    const newMeeting = {
      title: meetingTitle,
      location: location,
      start_date: new Date(startDate).toISOString(), 
      end_date: new Date(endDate).toISOString(),
      todo_id: "string",
      attendees: [attendee],
      created_by: "string"
    };

    try {
      const response = await axios.post('/meetings', newMeeting, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'application/json'
        },
        params: {
          token: token
        }
      });

      if (!response.data) {
        throw new Error("Failed to create new meeting");
      }

      const createdMeeting = response.data;
      setMeetings([...meetings, createdMeeting]);
      setMeetingTitle("");
      setLocation("");
      setAttendee({ user_id: "", status: "pending" });
      setStartDate("");
      setEndDate("");
    } catch (error) {
      console.error("Erro ao adicionar a reunião:", error.response ? error.response.data : error.message);
    }
  };

  return (
    <Box m="20px">
      <Header title="Meetings" subtitle="Create a New Meeting" />
      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            variant="filled"
            type="text"
            label="Meeting Title"
            value={meetingTitle}
            onChange={(e) => setMeetingTitle(e.target.value)}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            variant="filled"
            type="text"
            label="Location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </Grid>
        <Grid item xs={6} sm={6}>
          <TextField
            fullWidth
            variant="filled"
            type="datetime-local"
            label="Start Date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Grid>
        <Grid item xs={6} sm={6}>
          <TextField
            fullWidth
            variant="filled"
            type="datetime-local"
            label="End Date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            InputLabelProps={{
              shrink: true,
            }}
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            variant="filled"
            type="email"
            label="Attendee"
            value={attendee.user_id}
            onChange={(e) => setAttendee({ ...attendee, user_id: e.target.value })}
          />
        </Grid>
      </Grid>
      <Box display="flex" justifyContent="center" mt={2}>
        <Button size="large" onClick={addMeeting} color="secondary" variant="contained">
          Create New Meeting
        </Button>
      </Box>
    </Box>
  );
};

export default Meetings;
