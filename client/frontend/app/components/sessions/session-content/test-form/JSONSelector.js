import { useTestFormContext } from "@/app/components/contexts/session/test-form/TestFormContext";

export default function JSONSelector() {
  const { isJSON, setIsJSON, setSelectedBlocks } = useTestFormContext();
  return (
    <>
      <div className="form-check form-switch">
        <input
          className="form-check-input"
          type="checkbox"
          id="jsonToggle"
          checked={isJSON}
          onChange={() => {
            setIsJSON(!isJSON);
            setSelectedBlocks([]);
          }}
        />
        <label className="form-check-label ms-2" htmlFor="jsonToggle">
          {isJSON
            ? "Modalità file JSON attiva"
            : "Passa alla modalità file JSON"}
        </label>
      </div>
    </>
  );
}