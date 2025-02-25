import { useRouter } from "next/navigation";
import { useState } from "react";
import { useResponse } from "../contexts/ResponseContext";
import { useQuestionsContext } from "../contexts/QuestionsContext";
import Form from "next/form";
import { getCSRFToken } from "@/app/helpers/csrf";

const QnAForm = ({ sessionData }) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [formErrors, setFormErrors] = useState({});
  const [serverError, setServerError] = useState(null);
  const { setResponseData } = useResponse();
  const { selectedQuestions, setSelectedQuestions } = useQuestionsContext();
  const validateForm = () => {
    const errors = {};

    if (selectedQuestions.length == 0 && (!question || !answer)) {
      errors.question = "La domanda è obbligatoria.";
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
      var formatted = [];
      selectedQuestions.forEach((element) => {
        formatted.push({
          id: element.id,
          prompt_text: element.prompt_text,
          expected_answer: element.expected_answer,
        });
      });
      if (question !== "" && answer !== "") {
        formatted.push({
          prompt_text: question,
          expected_answer: answer,
        });
      }

      const response = await fetch("http://localhost:8000/runtest", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          data: formatted,
          sessionId: sessionData.id,
        }),
      });

      const data = await response.json();
      if (response.status === 503 || response.status === 500) {
        setServerError(data.error);
      } else {
        setResponseData(data);
        router.push(`/sessions/${sessionData.id}/results`);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card border-light rounded-5 w-md-75 mx-auto shadow-lg p-4 mb-5">
      <h3 className="card-title mb-4 text-center">Avvia un test</h3>
      <div className="text-center">
        {serverError && (
          <div className="alert alert-danger rounded-5" role="alert">
            {serverError}
          </div>
        )}
      </div>
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
          {formErrors.question && (
            <div className="invalid-feedback">{formErrors.question}</div>
          )}
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
          {formErrors.answer && (
            <div className="invalid-feedback">{formErrors.answer}</div>
          )}
        </div>

        <div className="text-center">
          {formErrors.llm && (
            <div className="alert alert-danger">{formErrors.llm}</div>
          )}

          <button
            type="submit"
            className="btn btn-primary w-50 rounded-5"
            disabled={loading}
          >
            {loading ? (
              <span
                className="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
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
