'use client'
import { SessionContext } from "@/app/components/contexts/SessionContext";
import { use, useState, useEffect, useContext } from "react";
import Form from 'next/form';

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
            <div className="text-center mb-5">
                <h1 className="display-4">Benvenuto alla sessione {sessionData.title}</h1>
                <p className="lead text-muted">{sessionData.description}</p>
                <h3 className="text-secondary mt-5 mb-4">Large Language Models connessi</h3>
            </div>
            <div className="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4 mb-5">
                {sessionData.llm.map((llm, index) => (
                    <div className="col" key={index}>
                        <div className="card shadow-sm border-light rounded-lg">
                            <div className="card-body">
                                <h5 className="card-title text-primary">{llm.name}</h5>
                                <p className="card-text text-muted">Number of Parameters: {llm.n_parameters}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="mt-5">
                <h3 className="text-center text-secondary mb-4">Fai una domanda</h3>
                <div className="row justify-content-center">
                    <div className="col-md-8">
                        <Form>
                            <div className="form-floating mb-3">
                                <input type="text" className="form-control rounded-5" id="question" name="question" placeholder="Titolo" />
                                <label htmlFor="question">Domanda</label>
                            </div>
                            <div className="form-floating mb-3">
                                <input type="text" className="form-control rounded-5" id="answer" name="answer" placeholder="Descrizione" />
                                <label htmlFor="answer">Risposta attesa</label>
                            </div>
                            <div className="text-center">
                                <button type="submit" className="btn btn-primary w-50 rounded-5">Invia</button>
                            </div>
                        </Form>
                    </div>
                </div>
            </div>
        </div>
    );
}
