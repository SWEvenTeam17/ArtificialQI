import React from "react";
import { useTestContext } from "../../contexts/SessionPageContext";
import Form from "next/form";
import delteIcon from "/public/images/icon.png";
import Image from "next/image";
export default function SessionLLMPanelContainer() {
  const {
    submitLLM,
    isLLMDataEmpty,
    remainingLLMs,
    sessionData,
    limit,
    deleteLLM,
  } = useTestContext();
  return (
    <div className="card border-0 h-100">
      <div className="card-body text-center">
        <h5 className="card-title text-center text-primary font-weight-bold">
          Gestisci LLM collegati
        </h5>
        <div className="row justify-content-center">
          <div className="col-md-6 col-12">
            <Form onSubmit={submitLLM} className="h-100">
              {limit && (
                <div className="alert alert-danger rounded-5" role="alert">
                  {limit}
                </div>
              )}
              <select
                className="form-select mt-4 mb-4 rounded-5 text-center"
                name="selectllm"
                id="selectllm"
                defaultValue={isLLMDataEmpty ? "no-llm" : ""}
                required
                disabled={isLLMDataEmpty}
              >
                <option value="">
                  {isLLMDataEmpty
                    ? "Nessun LLM disponibile"
                    : "Seleziona un LLM..."}
                </option>
                {!isLLMDataEmpty &&
                  remainingLLMs.map((llm) => (
                    <option key={llm.id} value={llm.id}>
                      {llm.name}
                    </option>
                  ))}
              </select>
              <button
                className="btn btn-primary rounded-5 w-100"
                type="submit"
                disabled={isLLMDataEmpty}
              >
                Aggiungi
              </button>
            </Form>
          </div>
        </div>
        {sessionData.llm.length > 0 ? (
          <div className="row row-cols-4 g-4 mb-5 mt-5">
            {sessionData.llm.map((llm) => (
              <div className="col-3" key={llm.id}>
                <div className="card rounded-5">
                  <div className="card-body">
                    <h5 className="card-title text-primary">{llm.name}</h5>
                    <p className="card-text text-muted">
                      Numero di Parametri: {llm.n_parameters}
                    </p>
                    <button
                      className="btn btn-danger w-50 rounded-5"
                      onClick={() => deleteLLM(llm.id)}
                    >
                      <Image
                        width={32}
                        height={32}
                        alt="Elimina llm"
                        src={delteIcon}
                      />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-5 text-center">
            <p className="text-secondary">
              Nessun LLM selezionato, aggiungi un LLM per cominciare.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
