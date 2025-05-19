import { useRouter } from "next/navigation";
import { useState } from "react";
import { useResponse } from "../contexts/ResponseContext";
import { useQuestionsContext } from "../contexts/QuestionsContext";
import { getCSRFToken } from "@/app/helpers/csrf";

const QnAForm = ({ sessionData }) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [blockName, setBlockName] = useState("");
  const [questionAnswerPairs, setQuestionAnswerPairs] = useState([
    { question: "", answer: "" },
  ]);
  const [formErrors, setFormErrors] = useState({});
  const [serverError, setServerError] = useState(null);
  const [isJSON, setIsJSON] = useState(false);
  const [jsonFile, setJsonFile] = useState(null);
  const { setResponseData } = useResponse();
  const { selectedQuestions } = useQuestionsContext();

  const validateForm = () => {
    const errors = {};
    questionAnswerPairs.forEach((pair, index) => {
      const pairErrors = {};
      if (!pair.question && selectedQuestions.length === 0)
        pairErrors.question = "La domanda è obbligatoria.";
      if (!pair.answer && selectedQuestions.length === 0)
        pairErrors.answer = "La risposta attesa è obbligatoria.";
      if (Object.keys(pairErrors).length > 0) errors[index] = pairErrors;
    });

    if (!sessionData.llm || sessionData.llm.length === 0) {
      errors.llm = "Aggiungi almeno un LLM per continuare.";
    }

    if (!blockName.trim()) {
      errors.blockName = "Il nome del test è obbligatorio.";
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

    await submitToBackend(questionAnswerPairs);
  };

  const submitToBackend = async (dataToSend) => {
    setLoading(true);
    setFormErrors({});
    setServerError(null);

    try {
      const formatted = [];

      selectedQuestions.forEach((element) => {
        formatted.push({
          id: element.id,
          prompt_text: element.prompt_text,
          expected_answer: element.expected_answer,
        });
      });

      dataToSend.forEach((pair) => {
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
            blockName: blockName.trim(),
          }),
        },
      );

      const data = await response.json();
      if (
        response.status === 503 ||
        response.status === 500 ||
        response.status === 400
      ) {
        setServerError(data.error);
      } else {
        setResponseData(data);
        router.push(`/sessions/${sessionData.id}/results`);
      }
    } catch (error) {
      console.error("Error submitting form:", error);
      setServerError(error);
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

  const handleJSONFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const parsed = JSON.parse(event.target.result);
          if (
            Array.isArray(parsed) &&
            parsed.every(
              (item) =>
                typeof item.question === "string" &&
                typeof item.answer === "string",
            )
          ) {
            setQuestionAnswerPairs(parsed);
            setServerError(null);
          } else {
            setServerError("Il file JSON non ha il formato corretto.");
          }
        } catch (error) {
          setServerError("Errore durante la lettura del file JSON.");
        }
      };
      reader.readAsText(file);
      setJsonFile(file);
    } else {
      setServerError("Inserisci un file JSON valido.");
    }
  };

  const handleJSONSubmit = async (e) => {
    e.preventDefault();
    if (!jsonFile || questionAnswerPairs.length === 0) {
      setServerError("Inserire un file JSON valido prima di avviare il test.");
      return;
    }

    await submitToBackend(questionAnswerPairs);
  };

  return (
    <div className="card border-0 w-md-75 mx-auto p-4">
      <h3 className="card-title mb-4 text-center">Avvia un test</h3>

      {serverError && (
        <div className="alert alert-danger text-center" role="alert">
          {serverError}
        </div>
      )}

      {isJSON ? (
        <form onSubmit={handleJSONSubmit} className="text-center">
          <div className="mb-3">
            <input
              type="file"
              accept=".json"
              onChange={handleJSONFileChange}
              className="form-control w-50 mx-auto"
            />
          </div>

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
        </form>
      ) : (
        <form onSubmit={handleSubmit}>
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

          {formErrors.llm && (
            <div className="alert alert-danger rounded-5 text-center">
              {formErrors.llm}
            </div>
          )}
          <div className="row row-cols-1">
            <div className="col-12">
              <div className="form-floating">
                <input
                  type="text"
                  className={`form-control rounded-5 ${formErrors.blockName ? "is-invalid" : ""}`}
                  id={`block_name`}
                  name="block_name"
                  value={blockName}
                  onChange={(e) => setBlockName(e.target.value)}
                  placeholder={`Inserisci un nome per questo test`}
                />
                <label htmlFor={`block_name`}>
                  Inserisci un nome per questo test
                </label>
                {formErrors.blockName && (
                  <div className="invalid-feedback">{formErrors.blockName}</div>
                )}
              </div>
            </div>
          </div>
          <div className="row row-cols-md-2 row-cols-1 g-3 mt-2 mb-3">
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
        </form>
      )}

      <div className="form-check form-switch mt-4">
        <input
          className="form-check-input"
          type="checkbox"
          id="jsonToggle"
          checked={isJSON}
          onChange={() => {
            setIsJSON(!isJSON);
            setServerError(null);
            setFormErrors({});
            setQuestionAnswerPairs([{ question: "", answer: "" }]);
          }}
        />
        <label className="form-check-label ms-2" htmlFor="jsonToggle">
          {isJSON
            ? "Modalità file JSON attiva"
            : "Passa alla modalità file JSON"}
        </label>
      </div>
    </div>
  );
};

export default QnAForm;
