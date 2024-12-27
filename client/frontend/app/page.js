'use client'
import { useContext } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import Link from 'next/link';

export default function Home() {
  const sessions = useContext(SessionContext);

  return (
  <div className="container">
    <h1 className="text-center display-1 fw-medium mt-5 p-5">ArtificialQI</h1>
    <p className="text-center fs-5">Per cominciare, seleziona una sessione:</p>
    <div className="row row-cols-lg-4 row-cols-2 mt-5 g-2">
      {sessions.map((session, index) => (
        <div key={index} className="col">
          <Link
          key={index}
          href={`/sessions/${session.id}`}
          className="card text-decoration-none text-center"
          >
            <h4 className="card-title p-1">{session.title}</h4>
            <p className="card-text p-1">{session.description}</p>
          </Link>
        </div>
      ))}
    </div>
  </div>);
}
