import React from "react";
import Form from "next/form";

export default function CreateLLMFormPresentational({formErrors, conflict, ollamaError, setName, setParameters, createLLM, loadOllamaModels, parameters, name}) {
  return (
    <div className="mt-5">
      <div>
        {conflict && (
          <div className="alert alert-danger rounded-5" role="alert">
            {conflict}
          </div>
        )}
      </div>
      <Form onSubmit={createLLM}>
        <p className="text-center fs-5">Crea un LLM:</p>
        <div className="row row-cols-md-2 row-cols-1 g-2">
          <div className="col">
            <div className="form-floating">
              <input
                type="text"
                id="name"
                name="name"
                className={`form-control rounded-5 ${formErrors.name ? "is-invalid" : ""}`}
                placeholder="Nome"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <label htmlFor="name">Nome</label>
              {formErrors.name && (
                <div className="invalid-feedback">{formErrors.name}</div>
              )}
            </div>
          </div>
          <div className="col">
            <div className="form-floating">
              <input
                type="text"
                id="nparameters"
                name="nparameters"
                className={`form-control rounded-5 ${formErrors.n_parameters ? "is-invalid" : ""}`}
                placeholder="Numero Parametri"
                value={parameters}
                onChange={(e) => setParameters(e.target.value)}
              />
              <label htmlFor="description">Numero Parametri</label>
              {formErrors.n_parameters && (
                <div className="invalid-feedback">
                  {formErrors.n_parameters}
                </div>
              )}
            </div>
          </div>
          <div className="col">
            <button type="submit" className="btn btn-primary w-100 rounded-5">
              Crea
            </button>
          </div>
          <div className="col">
            <button
              onClick={(e) => {
                loadOllamaModels(e);
              }}
              className="btn btn-outline-success w-100 rounded-5"
            >
              Carica modelli di Ollama
            </button>
          </div>
        </div>

        {ollamaError && (
          <div className="col-12 text-danger mt-2">{ollamaError}</div>
        )}
      </Form>
    </div>
  );
}
