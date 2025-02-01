'use client'
import { useContext } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import SessionCard from './components/sessions/SessionCard';

export default function Home() {
  const {sessions, deleteSession} = useContext(SessionContext);

  return (
    <div className="container">
      <h1 className="text-center display-1 fw-medium mt-5 p-5">ArtificialQI</h1>
      <p className="text-center fs-5">Per cominciare, seleziona una sessione:</p>
      <div className="row row-cols-lg-4 row-cols-2 mt-5 g-2">
        {sessions.map((session, index) => (
          <div className='col' key={index}>
            <SessionCard session={session} deleteSession={deleteSession} />
          </div>
        ))}
      </div>
    </div>
  );
}
