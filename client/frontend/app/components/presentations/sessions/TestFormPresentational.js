import PrevTests from "../../results/PrevTests";
import React from "react";
import TestResultsContainer from "../../containers/sessions/TestResultsContainer";

export default function TestFormPresentational({
  selectedBlocks,
  testResults,
  loading,
  questionBlocks,
  isSelected,
  removeBlock,
  addBlock,
  submitToBackend,
  setPrevTests,
  prevTests,
  activeView,
  showPrevTests,
  handlePrevTestClick,
}) {
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
