import { useState } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";

export const useCreateLLMFormHook = (fetchLLMList) => {
  const [formErrors, setFormErrors] = useState({});
  const [conflict, setConflict] = useState(null);
  const [ollamaError, setOllamaError] = useState("");
  const [name, setName] = useState("");
  const [parameters, setParameters] = useState("");

  const validateForm = () => {
    const errors = {};
    if (!name) errors.name = "Il nome è obbligatorio.";
    if (!parameters)
      errors.n_parameters = "Il numero di parametri è obbligatorio.";
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
    const data = { name, n_parameters: parameters };

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify(data),
        }
      );

      const responseData = await response.json();
      if (response.status === 409) {
        setConflict(responseData.error);
      } else {
        fetchLLMList();
        setName("");
        setParameters("");
        setConflict(null);
      }
    } catch (error) {
      console.error("Errore durante la creazione:", error);
    }
  };

  const loadOllamaModels = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/load_ollama/`,
        {
          method: "POST",
          headers: { "X-CSRFToken": getCSRFToken() },
        }
      );

      if (res.status === 200) {
        fetchLLMList();
        setOllamaError("");
      } else {
        setOllamaError("Connessione con il server Ollama fallita.");
      }
    } catch (err) {
      setOllamaError("Errore durante la connessione con Ollama.");
    }
  };

  return {
    name,
    parameters,
    setName,
    setParameters,
    formErrors,
    conflict,
    ollamaError,
    createLLM,
    loadOllamaModels,
  };
};
