import React, { useState, useCallback, useEffect } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
import TestResultsContainer from "./TestResultsContainer";
import PrevTests from "../../results/PrevTests";
export default function TestFormContainer({ sessionData }) {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null);
  const [selectedBlocks, setSelectedBlocks] = useState([]);
  const [error, setError] = useState(null); // 🔴 Nuovo stato per l'errore

  const addBlock = async (id) => {
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`
      );
      if (!response.ok) throw new Error("Errore nel recupero del blocco");
      let data = await response.json();
      setSelectedBlocks((prevBlocks) => [...prevBlocks, data]);
      setError(null);
    } catch (err) {
      setError("Errore durante l'aggiunta del blocco.");
    }
  };

  const removeBlock = (id) => {
    setSelectedBlocks((prevBlocks) =>
      prevBlocks.filter((block) => block.id !== id)
    );
    setError(null);
  };

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
      );
      if (!response.ok) throw new Error("Errore nel recupero dei blocchi");
      let data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0
      );
      setQuestionBlocks(filteredData);
      setError(null);
    } catch (error) {
      console.error(
        "Errore durante il recupero dei blocchi di domande:",
        error
      );
      setError("Impossibile caricare i blocchi di domande.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, [fetchQuestionBlocks]);

  const isSelected = (questionId) => {
    return selectedBlocks.some((q) => q.id === questionId);
  };

  const submitToBackend = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
            sessionId: sessionData.id,
            blocks: selectedBlocks,
          }),
        }
      );
      const data = await response.json();
      setTestResults(data);
      setActiveView("results");
      setError(null);
    } catch (error) {
      console.error("Errore durante l'esecuzione del test:", error);
      setError("Errore durante l'esecuzione del test:", error);
    } finally {
      setLoading(false);
    }
  };

  const showPrevTests = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/`
      );
      if (!response.ok)
        throw new Error("Errore nel recupero dei test precedenti");
      const data = await response.json();
      setPrevTests(data);
      setActiveView("prev");
      setError(null);
    } catch (error) {
      console.error("Errore nel recupero dei test precedenti:", error);
      setError("Errore nel recupero dei test precedenti.");
    }
  };

  const handlePrevTestClick = async (test) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`
      );
      if (!response.ok)
        throw new Error("Errore nel recupero del test selezionato");
      const data = await response.json();
      setTestResults(data);
      setActiveView("results");
      setError(null);
    } catch (error) {
      console.error("Errore caricando il test precedente:", error);
      setError("Errore caricando il test precedente.");
    }
  };

  return questionBlocks.length > 0 ? (
    <>
      {error && (
        <div className="alert alert-danger text-center" role="alert">
          {error}
        </div>
      )}
      <div className="card border-0">
        <div className="card-body">
          <h5 className="card-title text-center text-primary fw-bold">
            Blocchi di domande disponibili
          </h5>
          <ul
            className="list-group list-group-flush"
            style={{ maxHeight: "300px", overflowY: "auto" }}
          >
            {questionBlocks.map((block, index) => (
              <li
                key={index}
                className="list-group-item list-group-item-action rounded-3"
              >
                <div className="row">
                  <div className="col-9">
                    <p className="fw-bold mb-1">Nome</p>
                    <p>{block.name}</p>
                  </div>
                  <div className="col-md-3 col-12">
                    {isSelected(block.id) ? (
                      <button
                        className="btn btn-outline-success rounded-5 w-100 mb-2"
                        onClick={(e) => {
                          e.preventDefault();
                          removeBlock(block.id);
                        }}
                        disabled={loading}
                      >
                        Rimuovi
                      </button>
                    ) : (
                      <button
                        className="btn btn-success rounded-5 w-100 mb-2"
                        onClick={(e) => {
                          e.preventDefault();
                          addBlock(block.id);
                        }}
                        disabled={loading}
                      >
                        Seleziona
                      </button>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
        <div className="row row-cols-1 mt-5 g-0 justify-content-center text-center">
          <div className="col-md-6 col-12">
            <button
              onClick={(e) => {
                e.preventDefault();
                submitToBackend();
              }}
              className="btn btn-outline-primary w-50 rounded-5"
              disabled={loading || selectedBlocks.length === 0}
            >
              {loading ? (
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Caricamento...</span>
                </div>
              ) : (
                "Inizia il test"
              )}
            </button>
          </div>
          <div className="col-md-6 col-12">
            <button
              onClick={(e) => {
                e.preventDefault();
                showPrevTests();
              }}
              className="btn btn-outline-primary w-50 rounded-5"
            >
              Visualizza test precedenti
            </button>
          </div>
        </div>
      </div>
      {testResults && activeView === "results" && (
        <div className="card mt-4">
          <div className="card-body">
            <TestResultsContainer testResults={testResults} />
          </div>
        </div>
      )}
      {activeView === "prev" && (
        <div className="mt-4">
          <PrevTests
            prevTests={prevTests}
            setPrevTests={setPrevTests}
            onTestClick={handlePrevTestClick}
          />
        </div>
      )}
    </>
  ) : (
    <p className="text-center fs-3">
      È necessario creare dei blocchi di domande per eseguire un test.
    </p>
  );
}
