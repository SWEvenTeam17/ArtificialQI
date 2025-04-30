import { useRouter } from "next/navigation";
import { useState } from "react";
import { useResponse } from "../contexts/ResponseContext";
import { useQuestionsContext } from "../contexts/QuestionsContext";
import Form from "next/form";
import { getCSRFToken } from "@/app/helpers/csrf";

const QnAForm = ({ sessionData }) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [questionAnswerPairs, setQuestionAnswerPairs] = useState([
    { question: "", answer: "" },
  ]);
  const [formErrors, setFormErrors] = useState({});
  const [serverError, setServerError] = useState(null);
  const { setResponseData } = useResponse();
  const { selectedQuestions } = useQuestionsContext();

  const validateForm = () => {
    const errors = {};
    questionAnswerPairs.forEach((pair, index) => {
      const pairErrors = {};
      if (!pair.question && selectedQuestions.length === 0) pairErrors.question = "La domanda è obbligatoria.";
      if (!pair.answer && selectedQuestions.length === 0) pairErrors.answer = "La risposta attesa è obbligatoria.";
      if (Object.keys(pairErrors).length > 0) errors[index] = pairErrors;
    });

    if (!sessionData.llm || sessionData.llm.length === 0) {
      errors.llm = "Aggiungi almeno un LLM per continuare.";
    }

    return errors;
  };

  const hasError = (index, field) =>
    formErrors[index] && formErrors[index][field];

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
      const formatted = [];

      selectedQuestions.forEach((element) => {
        formatted.push({
          id: element.id,
          prompt_text: element.prompt_text,
          expected_answer: element.expected_answer,
        });
      });

      questionAnswerPairs.forEach((pair) => {
        if (pair.question && pair.answer) {
          formatted.push({
            prompt_text: pair.question,
            expected_answer: pair.answer,
          });
        }
      });

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
            data: formatted,
            sessionId: sessionData.id,
          }),
        }
      );

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

  const addQuestionAnswerPair = () => {
    setQuestionAnswerPairs([
      ...questionAnswerPairs,
      { question: "", answer: "" },
    ]);
  };

  const removeQuestionAnswerPair = (index) => {
    setQuestionAnswerPairs(questionAnswerPairs.filter((_, i) => i !== index));
  };

  const handleInputChange = (index, e) => {
    const { name, value } = e.target;
    const newArray = [...questionAnswerPairs];
    newArray[index][name] = value;
    setQuestionAnswerPairs(newArray);
  };

  return (
    <div className="card border-0 w-md-75 mx-auto p-4">
      <h3 className="card-title mb-4 text-center">Avvia un test</h3>
      <div className="text-center">
        {serverError && (
          <div className="alert alert-danger rounded-5" role="alert">
            {serverError}
          </div>
        )}
      </div>
      <Form onSubmit={handleSubmit}>
        {questionAnswerPairs.map((pair, index) => (
          <div key={index}>
            <div className="row align-items-center">
              <div className="col">
                <div className="form-floating">
                  <input
                    type="text"
                    className={`form-control rounded-5 ${
                      hasError(index, "question") ? "is-invalid" : ""
                    }`}
                    id={`question-${index}`}
                    name="question"
                    placeholder={`Domanda numero ${index}`}
                    value={pair.question}
                    onChange={(e) => handleInputChange(index, e)}
                  />
                  <label htmlFor={`question-${index}`}>
                    {`Domanda numero ${index + 1}`}
                  </label>
                  {hasError(index, "question") && (
                    <div className="invalid-feedback">
                      {formErrors[index].question}
                    </div>
                  )}
                </div>
              </div>
              <div className="col">
                <div className="form-floating">
                  <input
                    type="text"
                    className={`form-control rounded-5 ${
                      hasError(index, "answer") ? "is-invalid" : ""
                    }`}
                    id={`answer-${index}`}
                    name="answer"
                    placeholder={`Risposta attesa numero ${index + 1}`}
                    value={pair.answer}
                    onChange={(e) => handleInputChange(index, e)}
                  />
                  <label htmlFor={`answer-${index}`}>
                    {`Risposta attesa numero ${index + 1}`}
                  </label>
                  {hasError(index, "answer") && (
                    <div className="invalid-feedback">
                      {formErrors[index].answer}
                    </div>
                  )}
                </div>
              </div>
              {questionAnswerPairs.length > 1 && (
                <div className="col-auto">
                  <button
                    className="btn btn-danger"
                    onClick={(e) => {
                      e.preventDefault();
                      removeQuestionAnswerPair(index);
                    }}
                  >
                    X
                  </button>
                </div>
              )}
            </div>
            <hr />
          </div>
        ))}

        <div className="text-center">
          {formErrors.llm && (
            <div className="alert alert-danger rounded-5">
              {formErrors.llm}
            </div>
          )}

          <div className="row row-cols-md-2 row-cols-1 g-3">
            <div className="col">
              <button
                type="submit"
                className="btn btn-primary w-100 rounded-5"
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
            <div className="col">
              <button
                className="btn btn-outline-info w-100 rounded-5"
                onClick={(e) => {
                  e.preventDefault();
                  addQuestionAnswerPair();
                }}
              >
                Aggiungi una domanda
              </button>
            </div>
          </div>
        </div>
      </Form>
    </div>
  );
};

export default QnAForm;
