import Form from "next/form";
import { useCreateLLMFormHook } from "../hooks/LLM-Manager/CreateLLMFormHook";
import { useLLMManagerContext } from "../contexts/llm-manager/LLMManagerContext";
export default function CreateLLMForm() {
  const { fetchLLMList } = useLLMManagerContext();

  const {
    name,
    parameters,
    formErrors,
    conflict,
    ollamaError,
    setName,
    setParameters,
    createLLM,
    loadOllamaModels,
  } = useCreateLLMFormHook(fetchLLMList);

  return (
    <div className="mt-5">
      {conflict && (
        <div className="alert alert-danger rounded-5" role="alert">
          {conflict}
        </div>
      )}
      <Form onSubmit={createLLM}>
        <p className="text-center fs-5">Crea un LLM:</p>
        <div className="row row-cols-md-2 row-cols-1 g-2">
          <div className="col">
            <div className="form-floating">
              <input
                type="text"
                name="name"
                className={`form-control rounded-5 ${formErrors.name ? "is-invalid" : ""}`}
                placeholder="Nome"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
              <label>Nome</label>
              {formErrors.name && (
                <div className="invalid-feedback">{formErrors.name}</div>
              )}
            </div>
          </div>
          <div className="col">
            <div className="form-floating">
              <input
                type="text"
                name="nparameters"
                className={`form-control rounded-5 ${formErrors.n_parameters ? "is-invalid" : ""}`}
                placeholder="Numero Parametri"
                value={parameters}
                onChange={(e) => setParameters(e.target.value)}
              />
              <label>Numero Parametri</label>
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
              onClick={loadOllamaModels}
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
