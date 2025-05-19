import { useState, useEffect, useCallback } from "react";
import { useQuestionsContext } from "../contexts/QuestionsContext";
import { getCSRFToken } from "@/app/helpers/csrf";

const PreviousTestsCard = ({ id }) => {
  const [previousTests, setPreviousTests] = useState([]);
  const {
    selectedQuestions,
    setSelectedQuestions,
    addQuestion,
    removeQuestion,
  } = useQuestionsContext();

  const fetchPreviousTests = useCallback(async () => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${id}/`,
    );
    let data = await response.json();
    setPreviousTests(data);
  }, [id]);

  useEffect(() => {
    fetchPreviousTests();
  }, [fetchPreviousTests]);

  const deletePreviousTest = async (testId) => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${testId}/`,
      {
        method: "DELETE",
        body: JSON.stringify({ previousPromptId: testId }),
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      },
    );
    setPreviousTests((prevTests) => {
      return prevTests.filter((test) => test.id !== testId);
    });
  };

  const isSelected = (questionId) => {
    return selectedQuestions.some((q) => q.id === questionId);
  };

  return previousTests.length > 0 ? (
    <div className="card border-0">
      <div className="card-body">
        <h5 className="card-title text-center text-primary fw-bold">
          Test precedenti
        </h5>
        <ul
          className="list-group list-group-flush"
          style={{ maxHeight: "300px", overflowY: "auto" }}
        >
          {previousTests.map((pTest) => (
            <li
              key={pTest.id}
              className="list-group-item list-group-item-action rounded-3"
            >
              <div className="row">
                <div className="col-9">
                  <p className="fw-bold mb-1">Domanda</p>
                  <p>{pTest.prompt_text}</p>
                  <p className="fw-bold mb-1">Risposta attesa</p>
                  <p>{pTest.expected_answer}</p>
                </div>
                <div className="col-md-3 col-12">
                  {isSelected(pTest.id) ? (
                    <button
                      className="btn btn-outline-success rounded-5 w-100 mb-2"
                      onClick={(e) => {
                        e.preventDefault();
                        removeQuestion(pTest.id);
                      }}
                    >
                      Rimuovi
                    </button>
                  ) : (
                    <button
                      className="btn btn-success rounded-5 w-100 mb-2"
                      onClick={(e) => {
                        e.preventDefault();
                        addQuestion(pTest.id);
                      }}
                    >
                      Seleziona
                    </button>
                  )}
                  <button
                    className="btn btn-danger rounded-5 w-100"
                    onClick={(e) => {
                      e.preventDefault();
                      deletePreviousTest(pTest.id);
                    }}
                  >
                    Elimina
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  ) : null;
};

export default PreviousTestsCard;
