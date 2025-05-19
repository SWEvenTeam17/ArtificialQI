import { useState, useEffect } from "react";
import Form from "next/form";
import { getCSRFToken } from "@/app/helpers/csrf";

const AddLLMForm = ({ LLMData, sessionData, setSessionData, fetchLLMData }) => {
  const [limit, setLimit] = useState(null);
  const [isLLMDataEmpty, setIsLLMDataEmpty] = useState(
    !LLMData || LLMData.length === 0,
  );
  useEffect(() => {
    setIsLLMDataEmpty(!LLMData || LLMData.length === 0);
  }, [LLMData]);

  const submitLLM = async (e) => {
    e.preventDefault();

    if (sessionData.llm.length >= 3) {
      setLimit("Solo un massimo di 3 LLM è ammesso.");
    } else {
      const formData = new FormData(e.target);
      const data = {
        sessionId: sessionData.id,
        llmId: formData.get("selectllm"),
      };
      const JSONData = JSON.stringify(data);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_add/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSONData,
        },
      );
      const result = await response.json();
      setSessionData((prevSessionData) => ({
        ...prevSessionData,
        llm: [...prevSessionData.llm, result],
      }));
      fetchLLMData();
    }
  };

  return (
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
          {isLLMDataEmpty ? "Nessun LLM disponibile" : "Seleziona un LLM..."}
        </option>
        {!isLLMDataEmpty &&
          LLMData.map((llm) => (
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
  );
};

export default AddLLMForm;
