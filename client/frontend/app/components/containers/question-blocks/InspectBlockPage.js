import React from "react";
import { useState, useEffect } from "react";
import TestResultsContainer from "../sessions/TestResultsContainer";

export default function InspectBlockPage({ id }) {
  const [blockData, setBlockData] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [uniqueId, setUniqueId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBlockData = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}`
      );
      if (!response.ok) throw new Error("Errore nel recupero del blocco");
      const parsed = await response.json();
      setBlockData(parsed);
    } catch (err) {
      setError(err.message || "Errore sconosciuto");
    } finally {
      setLoading(false);
    }
  };

  const deletePrompt = async (promptId) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_list/${promptId}/`,
        {
          method: "DELETE",
        }
      );

      if (response.status === 204) {
        const updatedPrompts = blockData.prompt.filter(
          (prompt) => prompt.id !== promptId
        );
        setBlockData({ ...blockData, prompt: updatedPrompts });
      } else {
        console.error("Errore nella cancellazione del prompt");
      }
    } catch (err) {
      console.error("Errore nella richiesta:", err);
    }
  };

  const handleView = async (promptId) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_runs?prompt_id=${promptId}`
    );
    const data = await response.json();
    setUniqueId(promptId);
    setTestResults(data);
  };

  useEffect(() => {
    fetchBlockData();
  }, []);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border text-primary" role="status"></div>
        <p className="mt-3">Caricamento in corso...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger text-center mt-4" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="container py-4">
      <div className="text-center mb-4">
        <h1 className="text-primary">Blocco: {blockData.name}</h1>
        <h4 className="text-muted">
          Contiene {blockData.prompt?.length || 0} prompt
        </h4>
      </div>

      <div className="row row-cols-1 row-cols-md-2 g-4">
        {blockData.prompt?.map((prompt, index) => (
          <div className="col" key={index}>
            <div className="card shadow-sm h-100 border-primary">
              <div className="card-body">
                <h5 className="card-title">Domanda #{prompt.id}</h5>
                <p className="card-text">
                  <strong>Domanda:</strong> {prompt.prompt_text}
                </p>
                <p className="card-text">
                  <strong>Risposta attesa:</strong> {prompt.expected_answer}
                </p>
              </div>
              <div className="card-footer text-end">
                <button
                  className="btn btn-outline-primary btn-sm me-2"
                  onClick={() => handleView(prompt.id)}
                >
                  Visualizza run
                </button>
                <button
                  className="btn btn-outline-danger btn-sm"
                  onClick={() => deletePrompt(prompt.id)}
                >
                  Elimina prompt
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
      {testResults && (
        <TestResultsContainer key={uniqueId} testResults={testResults} />
      )}
    </div>
  );
}
