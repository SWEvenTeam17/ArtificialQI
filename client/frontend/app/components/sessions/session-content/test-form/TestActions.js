import { useSessionLLMContext } from "@/app/components/contexts/session/SessionLLMContext";
import { useTestFormContext } from "@/app/components/contexts/session/test-form/TestFormContext";

export default function TestActions() {
  const { submitToBackend, selectedBlocks, showPrevTests, loading } =
    useTestFormContext();
  const { sessionData } = useSessionLLMContext();
  return (
    <>
      <div className="card border-0 mb-5">
        <div className="row row-cols-1 mt-5 g-0 justify-content-center text-center">
          <div className="col-md-6 col-12">
            <button
              data-cy="run-test-button"
              onClick={(e) => {
                e.preventDefault();
                submitToBackend();
              }}
              className="btn btn-outline-primary w-50 rounded-5"
              disabled={
                loading ||
                selectedBlocks.length === 0 ||
                sessionData.llm?.length === 0
              }
            >
              {loading ? (
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Caricamento...</span>
                </div>
              ) : (
                "Inizia il test"
              )}
            </button>
          </div>
          <div className="col-md-6 col-12">
            <button
              onClick={(e) => {
                e.preventDefault();
                showPrevTests();
              }}
              className="btn btn-outline-primary w-50 rounded-5"
              data-cy="view-previous-tests"
            >
              Visualizza test precedenti
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
