/*import { CssBaseline, ThemeProvider } from "@mui/material";
import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import Login from "./login";
import Register from "./register";
import Calendar from "./scenes/calendar/calendar";
import Dashboard from "./scenes/dashboard";
import Documents from "./scenes/documents";
import Sidebar from "./scenes/global/Sidebar";
import Topbar from "./scenes/global/Topbar";
import Meetings from "./scenes/meetings";
import Notifications from "./scenes/noti";
import Inventory from "./scenes/todo";
import { ColorModeContext, useMode } from "./theme";

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false); // Authentication state management

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          {isAuthenticated && <Sidebar isSidebar={isSidebar} />}
          <main className="content">
            {isAuthenticated && <Topbar setIsSidebar={setIsSidebar} />}
            <Routes>
              <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
              <Route path="/register" element={<Register />} />
              {isAuthenticated ? (
                <>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/noti" element={<Notifications />} />
                  <Route path="/meetings" element={<Meetings />} />
                  <Route path="/documents" element={<Documents />} />
                  <Route path="/todo" element={<Inventory />} />
                  <Route path="/calendar" element={<Calendar />} />
                </>
              ) : (
                <Route path="*" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
              )}
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;*/

import { CssBaseline, ThemeProvider } from "@mui/material";
import { useState } from "react";
import { Route, Routes } from "react-router-dom";
import Calendar from "./scenes/calendar/calendar";
import Dashboard from "./scenes/dashboard";
import Documents from "./scenes/documents";
import Sidebar from "./scenes/global/Sidebar";
import Topbar from "./scenes/global/Topbar";
import Meetings from "./scenes/meetings";
import Notifications from "./scenes/noti";
import Inventory from "./scenes/todo";
import { ColorModeContext, useMode } from "./theme";

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <Sidebar isSidebar={isSidebar} />
          <main className="content">
            <Topbar setIsSidebar={setIsSidebar} />
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/noti" element={<Notifications />} />
              <Route path="/meetings" element={<Meetings />} />
              <Route path="/documents" element={<Documents />} />
              <Route path="/todo" element={<Inventory />} />
              <Route path="/calendar" element={<Calendar />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
