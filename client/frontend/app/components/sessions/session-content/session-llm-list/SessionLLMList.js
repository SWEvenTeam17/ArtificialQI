import { useTestContext } from "@/app/components/contexts/TestContext";
import SessionLLMCard from "./SessionLLMCard";
export default function SessionLLMList() {
  const { sessionData, deleteLLM } = useTestContext();
  return (
    <>
      {sessionData.llm.length > 0 ? (
        <div className="row row-cols-md-4 row-cols-1 g-4 mb-5 mt-5">
          {sessionData.llm.map((llm) => (
            <div className="col" key={llm.id}>
              <SessionLLMCard llm={llm} deleteLLM={deleteLLM} />
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
    </>
  );
}
