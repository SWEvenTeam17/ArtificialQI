import React from "react";
import CreateLLMFormPresentational from "../../presentations/LLM-Manager/CreateLLMFormPresentational";
import { useState } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
export default function CreateLLMFormContainer({ fetchLLMList }) {
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
    <CreateLLMFormPresentational
      name={name}
      formErrors={formErrors}
      conflict={conflict}
      ollamaError={ollamaError}
      setName={setName}
      setParameters={setParameters}
      createLLM={createLLM}
      parameters={parameters}
      loadOllamaModels={loadOllamaModels}
    />
  );
}
