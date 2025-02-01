'use client';
import { useEffect, useState } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import Script from 'next/script';
import Navbar from './components/layout/Navbar';
import './bootstrap.css';

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

  const onSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      title: formData.get('title'),
      description: formData.get('description'),
    };

    const JSONData = JSON.stringify(data);

    try {
      await fetch('http://localhost:8000/session_list/', {
        method: 'POST',
        headers: { "Content-type": "application/json" },
        body: JSONData,
      });

      fetchSessions();
      event.target.reset();
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const deleteSession = async(id)=>{
    let data = {
      id: id
    };
    const JSONData = JSON.stringify(data);
    try{
      await fetch(`http://localhost:8000/session_list/${id}/`,{
        method: 'DELETE',
        headers: {"Content-type": "application/josn"},
        body: JSONData
      });
      fetchSessions();

    } catch(error){
      console.error("Error deleting form: ",error);
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
          <Navbar sessions={sessions} onFormSubmit={onSubmit}/>
          <SessionContext.Provider value={{sessions, deleteSession}}>{children}</SessionContext.Provider>
        </main>
      </body>
    </html>
  );
}
