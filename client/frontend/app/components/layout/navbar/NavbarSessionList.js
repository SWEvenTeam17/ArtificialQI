import { useSessionContext } from "@/app/components/contexts/SessionContext";
import NavbarSessionElement from "./NavbarSessionElement";

export default function NavbarSessionList() {
  const { sessions } = useSessionContext();

  return (
    <div className="mt-4">
      <ul className="list-group">
        {sessions.map((session) => (
          <NavbarSessionElement key={session.id} session={session} />
        ))}
      </ul>
    </div>
  );
}
