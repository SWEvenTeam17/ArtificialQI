import { useSessionContext } from "../contexts/session/SessionContext";
import { useTestComparatorContext } from "../contexts/test-comparator/TestComparatorContext";

export default function SessionSelector() {
  const { sessions } = useSessionContext();
  const { setSelectedSessionData, fetchSessionData } =
    useTestComparatorContext();
  return (
    <select data-cy="session-select"
      onChange={(e) => {
        e.target.value === "0"
          ? setSelectedSessionData([])
          : fetchSessionData(e.target.value);
      }}
      className="form-select"
    >
      <option value="0">Seleziona una sessione</option>
      {sessions.map((session, index) => (
        <option key={index} value={session.id}>
          {session.title}
        </option>
      ))}
    </select>
  );
}
