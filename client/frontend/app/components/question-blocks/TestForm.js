import React, { useState, useEffect, useCallback } from "react";
import { useBlocksContext } from "../contexts/BlocksContext";
import { getCSRFToken } from "@/app/helpers/csrf";
import TestResults from "../results/TestResults";
import PrevTests from "../results/PrevTests";

const TestForm = ({ sessionData }) => {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const { selectedBlocks, addBlock, removeBlock } = useBlocksContext();
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null); // null | "prev" | "results"

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`,
      );
      let data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0,
      );
      setQuestionBlocks(filteredData);
    } catch (error) {
      console.error(
        "Errore durante il recupero dei blocchi di domande:",
        error,
      );
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
        },
      );
      const data = await response.json();
      setActiveView("results");
      setTestResults(data);
    } catch (error) {
      console.error("Errore durante l'esecuzione del test:", error);
    } finally {
      setLoading(false);
    }
  };

  const showPrevTests = async () => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/`,
    );
    const data = await response.json();
    setPrevTests(data);
    setActiveView("prev");
  };

  const handlePrevTestClick = async (test) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`,
    );
    const data = await response.json();
    console.log(data);
    setTestResults(data);
    setActiveView("results");
  }

  return questionBlocks.length > 0 ? (
    <>
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
            <TestResults testResults={testResults} />
          </div>
        </div>
      )}
      {activeView === "prev" && (
        <div className="mt-4">
          <PrevTests prevTests={prevTests} onTestClick={handlePrevTestClick} />
        </div>
      )}
    </>
  ) : null;
};

export default TestForm;
