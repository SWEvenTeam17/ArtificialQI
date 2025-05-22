import { useTestComparatorContext } from "../contexts/TestComparatorContext";

export default function LLMSelector() {
  const { setSelectedLLMS, selectedSessionData, selectedLLMS } =
    useTestComparatorContext();
  return (
    <div className="row row-cols-md-2 row-cols-1 p-3">
      <div className="col">
        <select
          onChange={(e) => {
            e.target.value !== "0"
              ? setSelectedLLMS((prev) => ({
                  ...prev,
                  firstLLM: e.target.value,
                }))
              : setSelectedLLMS((prev) => ({ ...prev, firstLLM: "" }));
          }}
          className="form-select"
        >
          <option value="0">Seleziona un LLM</option>
          {selectedSessionData.llm
            .filter((llm) => llm.id != selectedLLMS.secondLLM)
            .map((llm, index) => (
              <option value={llm.id} key={index}>
                {llm.name}
              </option>
            ))}
        </select>
      </div>
      <div className="col">
        <select
          onChange={(e) => {
            e.target.value !== "0"
              ? setSelectedLLMS((prev) => ({
                  ...prev,
                  secondLLM: e.target.value,
                }))
              : setSelectedLLMS((prev) => ({ ...prev, secondLLM: "" }));
          }}
          className="form-select"
        >
          <option value="0">Seleziona un LLM</option>
          {selectedSessionData.llm
            .filter((llm) => llm.id != selectedLLMS.firstLLM)
            .map((llm, index) => (
              <option value={llm.id} key={index}>
                {llm.name}
              </option>
            ))}
        </select>
      </div>
    </div>
  );
}
