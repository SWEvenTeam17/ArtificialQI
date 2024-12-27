'use client'
import { useEffect, useState } from 'react';
import Link from 'next/link';

export default function Home() {

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

  return (
  <div className="container">
    <h1 className="text-center display-1 fw-medium mt-5 p-5">ArtificialQI</h1>
    <p className="text-center fs-5">Per cominciare, seleziona una sessione:</p>
    <div className="row row-cols-lg-4 row-cols-2 mt-5">
      {sessions.map((session, index) => (
        <div key={index} className="col">
          <Link
          key={index}
          href={`/sessions/${session.id}`}
          className="card text-decoration-none text-center"
          >
            <h4 className="card-title p-1">{session.title}</h4>
          </Link>
        </div>
      ))}
    </div>
  </div>);
}
