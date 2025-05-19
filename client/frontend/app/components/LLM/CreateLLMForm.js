import { getCSRFToken } from "@/app/helpers/csrf";
import Form from "next/form";
import { useState } from "react";

const CreateLLMForm = ({ fetchLLMList }) => {
  const [formErrors, setFormErrors] = useState({});
  const [conflict, setConflict] = useState(null);
  const [name, setName] = useState("");
  const [parameters, setParameters] = useState("");
  const [ollamaError, setOllamaError] = useState("");

  const validateForm = () => {
    const errors = {};

    if (!name) {
      errors.name = "Il nome è obbligatorio.";
    }

    if (!parameters) {
      errors.n_parameters = "Il numero di parametri è obbligatorio.";
    }

    return errors;
  };

  const createLLM = async (e) => {
    e.preventDefault();
    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors({});

    const formData = new FormData(e.target);
    const data = {
      name: formData.get("name"),
      n_parameters: formData.get("nparameters"),
    };

    const JSONData = JSON.stringify(data);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSONData,
        },
      );

      const responseData = await response.json();
      if (response.status === 409) {
        setConflict(responseData.error);
      }

      fetchLLMList();
      setName("");
      setParameters("");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  const loadOllamaModels = async (e) => {
    e.preventDefault();
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/load_ollama/`,
      {
        method: "POST",
        headers: { "X-CSRFToken": getCSRFToken() },
      },
    );
    if (response.status === 200) {
      fetchLLMList();
    } else {
      setOllamaError("Connessione con il server Ollama fallita.");
    }
  };

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
};

export default CreateLLMForm;
