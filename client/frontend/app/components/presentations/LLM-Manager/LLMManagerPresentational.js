import CreateLLMForm from "../../llm-manager/CreateLLMForm";
import GeneralLLMCardContainer from "../../containers/LLM-Manager/GeneralLLMCardContainer";
export default function LLMManagerPresentational({ fetchLLMList, LLMList }) {
  return (
    <div className="card border-0 rounded-5 mt-3">
      <div className="card-body">
        <h2 className="card-title text-center">Gestisci LLM</h2>
        <div className="row mb-5 justify-content-center">
          <div className="col-12 col-md-6">
            <CreateLLMForm fetchLLMList={fetchLLMList} />
          </div>
        </div>
        <h2 className="card-title text-center mb-4">
          LLM collegati ad ArtificialQI
        </h2>
        {LLMList.length > 0 ? (
          <div className="row g-2 row-cols-1 row-cols-md-2">
            {LLMList.map((llm) => (
              <div className="col" key={llm.id}>
                <GeneralLLMCardContainer
                  llm={llm}
                  fetchLLMList={fetchLLMList}
                />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-center">Nessun LLM disponibile</p>
        )}
      </div>
    </div>
  );
}
