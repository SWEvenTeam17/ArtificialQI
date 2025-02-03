import { useRouter } from "next/navigation";
import { useState } from "react";
import { useResponse } from "../contexts/ResponseContext";
import Form from "next/form";

const QnAForm = ({ sessionData }) => {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const { setResponseData } = useResponse();

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
            router.push(`/sessions/${sessionData.id}/results`);

        } catch (error) {
            console.error("Error submitting form:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h3 className="card-title mb-4 text-center">Avvia un test</h3>

            <Form onSubmit={handleSubmit}>
                <div className="form-floating mb-4">
                    <input
                        type="text"
                        className="form-control rounded-5"
                        id="question"
                        name="question"
                        placeholder="Domanda"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        required
                    />
                    <label htmlFor="question">Domanda</label>
                </div>
                <div className="form-floating mb-4">
                    <input
                        type="text"
                        className="form-control rounded-5"
                        id="answer"
                        name="answer"
                        placeholder="Risposta attesa"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        required
                    />
                    <label htmlFor="answer">Risposta attesa</label>
                </div>
                <div className="text-center">
                    {sessionData.llm.length > 0 ? (
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
                    ) : (
                        <button className="btn btn-secondary w-50 rounded-5" disabled>
                            Aggiungi almeno un LLM per continuare...
                        </button>
                    )}
                </div>
            </Form>
        </div>
    );
};

export default QnAForm;
