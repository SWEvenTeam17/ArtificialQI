"use client";
import { useContext } from "react";
import { SessionContext } from "./components/contexts/SessionContext";
import SessionCard from "./components/sessions/SessionCard";

export default function Home() {
  const { sessions, deleteSession } = useContext(SessionContext);

  return (
    <div className="container">
      <h1 className="text-center display-1 fw-medium mt-5 p-5">ArtificialQI</h1>
      <p className="text-center fs-5">
        Per cominciare, seleziona una sessione:
      </p>
      <div className="row row-cols-md-2 row-cols-1 mt-5 g-2">
        {sessions.map((session) => (
          <div className="col" key={session.id}>
            <SessionCard session={session} deleteSession={deleteSession} />
          </div>
        ))}
      </div>
    </div>
  );
}
