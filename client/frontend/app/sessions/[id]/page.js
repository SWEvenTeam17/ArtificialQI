'use client'
import { SessionContext } from "@/app/components/contexts/SessionContext";
import { use, useState, useEffect, useContext } from "react"

export default function SessionPage({ params }) {
    const { id } = use(params);
    const sessions = useContext(SessionContext);
    const [sessionData, setSessionData] = useState(null);

    useEffect(() => {
        let data = sessions.find((data) => data.id == id);
        if (data) {
            setSessionData(data);
        }
        else {
            fetch(`http://localhost:8000/session_list/${id}`).then((response) => response.json()).then((data) => setSessionData(data)).catch((error) => {
                console.error("Error fetching session data:", error);
                setSessionData(null);
            });
        }

    }, [id, sessions]);

    if (sessionData === null) {
        return (
            <div className="d-flex justify-content-center align-items-center" style={{ height: "100vh", backgroundColor: "#f8f9fa" }}>
                <div className="spinner-grow text-secondary" style={{ width: "6rem", height: "6rem" }} role="status">
                    <span className="visually-hidden">Loading...</span>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <div className="text-center">
                <h1>Benvenuto alla sessione {sessionData.title}</h1>
                <p>{sessionData.description}</p>
            </div>
            <div className="row row-cols-1 row-cols-md-4">
                {sessionData.llm.map((llm, index) => (
                    <div className="col" key={index}>
                        <div className="card">
                            <div className="card-body">
                                <h5 className="card-title">{llm.name}</h5>
                                <p className="card-text">Number of Parameters: {llm.n_parameters}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

}