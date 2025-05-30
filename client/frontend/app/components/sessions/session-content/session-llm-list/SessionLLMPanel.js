import SessionLLMForm from "./SessionLLMForm";
import SessionLLMList from "./SessionLLMList";
export default function SessionLLMPanel() {
  return (
    <div className="card border-0 h-100">
      <div className="card-body text-center">
        <h5 className="card-title text-center text-primary font-weight-bold">
          Gestisci LLM collegati
        </h5>
        <div className="row justify-content-center">
          <div className="col-md-6 col-12">
            <SessionLLMForm />
          </div>
        </div>
        <SessionLLMList />
      </div>
    </div>
  );
}
