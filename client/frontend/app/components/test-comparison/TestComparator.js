import SessionSelector from "./SessionSelector";
import LLMSelector from "./LLMSelector";
import LLMComparisonChart from "./LLMComparisonChart";
import { useTestComparatorContext } from "../contexts/test-comparator/TestComparatorContext";
export default function TestComparatorContainer() {
  const { selectedSessionData, selectedLLMS, chartData } =
    useTestComparatorContext();
  return (
    <div className="container-fluid p-5">
      <div className="row text-center justify-content-center">
        <div className="col-md-6 col-12">
          <SessionSelector />
        </div>
      </div>
      {selectedSessionData.length !== 0 && <LLMSelector />}
      {selectedLLMS.firstLLM &&
        selectedLLMS.secondLLM &&
        chartData.length > 0 && <LLMComparisonChart />}
    </div>
  );
}
