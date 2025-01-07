'use client'
import { SessionContext } from "@/app/components/contexts/SessionContext";
import { use, useContext } from "react"

export default function SessionPage({ params }) {
    const { id } = use(params);
    const sessions = useContext(SessionContext);
    console.log(sessions);
    const sessionData = sessions.find((data) => {
        return data.id == id;
    });
    console.log(sessionData);

    return (
        <div className="container">
            <p>Benvenuto alla sessione {sessionData.id}</p>
            <p>Titolo: {sessionData.title}</p>
            <p>Descrizione: {sessionData.description}</p>
        </div>
    )
}