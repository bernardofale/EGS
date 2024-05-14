import React, { useState } from "react";
import { Box, Button, TextField, Select, MenuItem, Grid } from "@mui/material";
import Header from "../../components/Header";

const Meetings = () => {
  const [meetings, setMeetings] = useState([]);
  const [meetingTitle, setMeetingTitle] = useState("");
  const [day, setDay] = useState("");
  const [month, setMonth] = useState("");
  const [year, setYear] = useState("");
  const [hour, setHour] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");

  const addMeeting = () => {
    const newMeeting = {
      id: meetings.length + 1,
      title: meetingTitle,
      dateTime: `${day}/${month}/${year} ${hour}:00`,
      location: location,
      description: description,
    };
    setMeetings([...meetings, newMeeting]);
    // Reset form fields
    setMeetingTitle("");
    setDay("");
    setMonth("");
    setYear("");
    setHour("");
    setLocation("");
    setDescription("");
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
        <Grid item xs={6} sm={3}>
          <Select
            fullWidth
            variant="filled"
            value={day}
            onChange={(e) => setDay(e.target.value)}
            displayEmpty
            sx={{ textAlign: "center" }} // Center text
          >
            <MenuItem value="">Day</MenuItem>
            {Array.from({ length: 31 }, (_, i) => i + 1).map((day) => (
              <MenuItem key={day} value={day}>
                {day}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Select
            fullWidth
            variant="filled"
            value={month}
            onChange={(e) => setMonth(e.target.value)}
            displayEmpty
            sx={{ textAlign: "center" }} // Center text
          >
            <MenuItem value="">Month</MenuItem>
            {[
              "January",
              "February",
              "March",
              "April",
              "May",
              "June",
              "July",
              "August",
              "September",
              "October",
              "November",
              "December"
            ].map((month, index) => (
              <MenuItem key={index} value={index + 1}>
                {month}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Select
            fullWidth
            variant="filled"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            displayEmpty
            sx={{ textAlign: "center" }} // Center text
          >
            <MenuItem value="">Year</MenuItem>
            {Array.from({ length: 7 }, (_, i) => new Date().getFullYear() + i).map((year) => (
              <MenuItem key={year} value={year}>
                {year}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={6} sm={3}>
          <Select
            fullWidth
            variant="filled"
            value={hour}
            onChange={(e) => setHour(e.target.value)}
            displayEmpty
            sx={{ textAlign: "center" }} // Center text
          >
            <MenuItem value="">Hour</MenuItem>
            {Array.from({ length: 24 }, (_, i) => i).map((hour) => (
              <MenuItem key={hour} value={hour}>
                {hour < 10 ? `0${hour}:00` : `${hour}:00`}
              </MenuItem>
            ))}
          </Select>
        </Grid>
        <Grid item xs={12}>
          <TextField
            fullWidth
            variant="filled"
            type="text"
            label="Description"
            multiline
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            sx={{ marginBottom: 4 }}
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
