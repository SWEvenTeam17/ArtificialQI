import Form from "next/form";
import { useSessionLLMContext } from "@/app/components/contexts/session/SessionLLMContext";
export default function SessionLLMForm() {
  const { submitLLM, isLLMDataEmpty, remainingLLMs, limit } =
    useSessionLLMContext();
  return (
    <>
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
    </>
  );
}
