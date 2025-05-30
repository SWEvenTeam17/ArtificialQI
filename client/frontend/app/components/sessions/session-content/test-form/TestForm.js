import TestResults from "../TestResults";
import PrevTests from "../../../results/PrevTests";
import JSONView from "./JSONView";
import JSONSelector from "./JSONSelector";
import TestActions from "./TestActions";
import QuestionBlocksSelector from "./QuestionBlocksSelector";
import { useTestFormContext } from "@/app/components/contexts/session/test-form/TestFormContext";
export default function TestForm() {
  const { questionBlocks, error, isJSON, testResults, activeView } =
    useTestFormContext();

  return (
    <>
      <div className="card border-0">
        <div className="card-body">
          <JSONSelector />
        </div>
      </div>

      {isJSON && <JSONView />}

      {error && (
        <div className="alert alert-danger text-center" role="alert">
          {error}
        </div>
      )}

      {!isJSON && questionBlocks.length > 0 && <QuestionBlocksSelector />}

      {!isJSON && questionBlocks.length === 0 && (
        <p className="text-center fs-3">
          È necessario creare dei blocchi di domande per eseguire un test.
        </p>
      )}
      <TestActions />
      {testResults && activeView === "results" && (
        <div className="card mt-4">
          <div className="card-body">
            <TestResults />
          </div>
        </div>
      )}
      {activeView === "prev" && (
        <div className="mt-4">
          <PrevTests />
        </div>
      )}
    </>
  );
}
