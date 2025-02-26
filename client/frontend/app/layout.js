"use client";
import { useEffect, useState } from "react";
import { SessionContext } from "./components/contexts/SessionContext";
import Script from "next/script";
import Navbar from "./components/layout/Navbar";
import "./bootstrap.css";
import { getCSRFToken } from "./helpers/csrf";

export default function RootLayout({ children }) {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/session_list");
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  const deleteSession = async (id) => {
    let data = {
      id: id,
    };
    const JSONData = JSON.stringify(data);
    try {
      await fetch(`http://backend:8000/session_list/${id}/`, {
        method: "DELETE",
        headers: {
          "Content-type": "application/josn",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSONData,
      });
      fetchSessions();
    } catch (error) {
      console.error("Error deleting form: ", error);
    }
  };

  return (
    <html lang="en">
      <body>
        <header>
          <Script src="/scripts/bootstrap.bundle.js"></Script>
          <title>ArtificialQI</title>
        </header>
        <main>
          <Navbar sessions={sessions} fetchSessions={fetchSessions} />
          <SessionContext.Provider value={{ sessions, deleteSession }}>
            {children}
          </SessionContext.Provider>
        </main>
      </body>
    </html>
  );
}
