import React from "react";
import TestResults from "../../results/TestResults";
import TestResultsPresentational from "../sessions/TestResultsPresentational";
import TestResultsContainer from "../../containers/sessions/TestResultsContainer";

export default function InspectBlockPagePresentational({
  blockData,
  loading,
  error,
  deletePrompt,
  handleView,
  testResults,
  uniqueId,
}) {
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
      {testResults && <TestResultsContainer key={uniqueId} testResults={testResults} />}
    </div>
  );
}
