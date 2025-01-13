'use client'
import { use, useState, useEffect, useContext } from "react";
import { SessionContext } from "@/app/components/contexts/SessionContext";
import { useResponse } from "@/app/components/contexts/ResponseContext";
import { useRouter } from "next/navigation";
import Form from 'next/form';

export default function SessionPage({ params }) {
    const router = useRouter();
    const { id } = use(params);
    const sessions = useContext(SessionContext);
    const [sessionData, setSessionData] = useState(null);
    const [LLMData, setLLMData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const { setResponseData } = useResponse();

    useEffect(() => {
        // let data = sessions.find((data) => data.id == id);
        // if (data) {
        //     setSessionData(data);
        // }
        // else {
        //     fetch(`http://localhost:8000/session_list/${id}`)
        //         .then((response) => response.json())
        //         .then((data) => setSessionData(data))
        //         .catch((error) => {
        //             console.error("Error fetching session data:", error);
        //             setSessionData(null);
        //         });
        // }
        fetchSessionData();
    }, [id, sessions]);

    useEffect(() => {
        fetch(`http://localhost:8000/llm_list/`)
            .then((response) => response.json())
            .then((data) => setLLMData(data))
            .catch((error) => {
                console.error("Error fetching LLM data:", error);
                setLLMData([]);
            });
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch("http://localhost:8000/runtest", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question: question, answer: answer, sessionId: sessionData.id }),
            });

            const data = await response.json();
            console.log(data);
            setResponseData(data.responses);
            router.push(`/sessions/${id}/results`);

        } catch (error) {
            console.error("Error submitting form:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmitLLM = (llm) => {
        sessionData.llm = [... llm];
    };

    const submitLLM = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            sessionId: sessionData.id,
            llmId: formData.get('selectllm')
        }
        const JSONData = JSON.stringify(data);

        try {
            const response = await fetch("http://localhost:8000/llm_add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSONData
            });
            const result = await response.json();
            console.log(result);
            fetchSessionData();
        } catch (error) {
            console.error("Error adding LLM:", error);
        }
    };

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
            <h3 className="text-secondary mt-4">Large Language Models connessi</h3>
            <Form onSubmit={submitLLM}>
                <select 
                className="form-select"
                name="selectllm"
                id="selectllm"
                defaultValue=""
                required
                >
                    <option value="" disabled>
                        Seleziona un LLM...
                    </option>
                    {LLMData.map((llm, index) => (
                        <option key={index} value={llm.id}>{llm.name}</option>
                    ))}
                </select>
                <button className="btn btn-primary" type="submit">
                    Aggiungi
                </button>
            </Form>
            <div className="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4 mb-5 p-5">
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
            <div className="text-center justify-content-center">
                <Form onSubmit={handleSubmit}>
                    <div className="form-floating mb-3">
                        <input
                            type="text"
                            className="form-control rounded-5"
                            id="question"
                            name="question"
                            placeholder="Domanda"
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                        />
                        <label htmlFor="question">Domanda</label>
                    </div>
                    <div className="form-floating mb-3">
                        <input
                            type="text"
                            className="form-control rounded-5"
                            id="answer"
                            name="answer"
                            placeholder="Risposta attesa"
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                        />
                        <label htmlFor="answer">Risposta attesa</label>
                    </div>
                    <div className="text-center align-items-center col-12">
                        <button
                            type="submit"
                            className="btn btn-primary w-50 rounded-5"
                            disabled={loading}
                        >
                            {loading ? (
                                <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                            ) : (
                                "Invia"
                            )}
                        </button>
                    </div>
                </Form>
            </div>
        </div>
    );
}
