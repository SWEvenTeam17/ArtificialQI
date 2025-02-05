import { useRouter } from "next/navigation";
import { useState } from "react";
import { useResponse } from "../contexts/ResponseContext";
import Form from "next/form";

const QnAForm = ({ sessionData }) => {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [formErrors, setFormErrors] = useState({});
    const { setResponseData } = useResponse();

    const validateForm = () => {
        const errors = {};
        
        if (!question) {
            errors.question = "La domanda è obbligatoria.";
        }

        if (!answer) {
            errors.answer = "La risposta attesa è obbligatoria.";
        }

        if (!sessionData.llm || sessionData.llm.length === 0) {
            errors.llm = "Aggiungi almeno un LLM per continuare.";
        }

        return errors;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const errors = validateForm();
        if (Object.keys(errors).length > 0) {
            setFormErrors(errors);
            return;
        }

        setLoading(true);
        setFormErrors({});

        try {
            const response = await fetch("http://localhost:8000/runtest", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    question: question,
                    answer: answer,
                    sessionId: sessionData.id,
                }),
            });

            const data = await response.json();
            console.log(data);
            setResponseData(data.response);
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
                        className={`form-control rounded-5 ${formErrors.question ? "is-invalid" : ""}`}
                        id="question"
                        name="question"
                        placeholder="Domanda"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                    />
                    <label htmlFor="question">Domanda</label>
                    {formErrors.question && <div className="invalid-feedback">{formErrors.question}</div>}
                </div>

                <div className="form-floating mb-4">
                    <input
                        type="text"
                        className={`form-control rounded-5 ${formErrors.answer ? "is-invalid" : ""}`}
                        id="answer"
                        name="answer"
                        placeholder="Risposta attesa"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                    />
                    <label htmlFor="answer">Risposta attesa</label>
                    {formErrors.answer && <div className="invalid-feedback">{formErrors.answer}</div>}
                </div>

                <div className="text-center">
                    {formErrors.llm && <div className="alert alert-danger">{formErrors.llm}</div>}

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
    );
};

export default QnAForm;
