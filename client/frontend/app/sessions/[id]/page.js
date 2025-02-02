'use client'
import { use, useState, useEffect, useContext } from "react";
import { SessionContext } from "@/app/components/contexts/SessionContext";
import AddLLMForm from "@/app/components/LLM/AddLLMForm";
import LLMCard from "@/app/components/LLM/LLMCard";
import QnAForm from "@/app/components/prompt/QnAForm";

export default function SessionPage({ params }) {
    const { id } = use(params);
    const {sessions} = useContext(SessionContext);
    const [sessionData, setSessionData] = useState(null);
    const [LLMData, setLLMData] = useState(null);

    useEffect(() => {
        fetchSessionData();
    }, []);

    useEffect(() => {
        fetchLLMData();
    }, []);

    const fetchSessionData = async () => {
        let data = sessions.find((data) => data.id == id);
        if (data) {
            setSessionData(data);
        }
        else {
            fetch(`http://localhost:8000/session_list/${id}`)
                .then((response) => response.json())
                .then((data) => setSessionData(data))
                .catch((error) => {
                    console.error("Error fetching session data:", error);
                    setSessionData(null);
                });
        }
    };

    const fetchLLMData = async () => {
        fetch(`http://localhost:8000/llm_remaining/${id}`)
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                setLLMData(Array.isArray(data) ? data : []);
            })
            .catch((error) => {
                console.error("Error fetching LLM data:", error);
                setLLMData([]);
            });
    }

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
                <h1>Benvenuto alla sessione {sessionData.title}</h1>
                <p>{sessionData.description}</p>
            </div>
            <div className="d-flex justify-content-center align-items-center">
            <AddLLMForm LLMData={LLMData} sessionData={sessionData} setSessionData={setSessionData} fetchLLMData={fetchLLMData} />
            </div>
            {sessionData.llm.length > 0 ? (
                <div className="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4 mb-5 p-5">
                    {sessionData.llm.map((llm, index) => (
                        <div className="col" key={index}>
                            <LLMCard id={id} llm={llm} fetchLLMData={fetchLLMData} setSessionData={setSessionData} />
                        </div>
                    ))}
                </div>
            ) : (
                <div className="p-5 text-center">
                    <p>Nessun LLM selezionato, aggiungi un LLM per cominciare.</p>
                </div>
            )}
            <div className="text-center justify-content-center">
                <QnAForm sessionData={sessionData} />
            </div>
        </div>
    );
}
