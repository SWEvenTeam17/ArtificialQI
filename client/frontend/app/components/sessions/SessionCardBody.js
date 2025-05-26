import Link from "next/link";
import { useSessionCard } from "@/app/components/contexts/session/SessionCardContext";

export default function SessionCardBody() {
  const {
    session,
    isEditing,
    editedTitle,
    editedDescription,
    setEditedTitle,
    setEditedDescription,
  } = useSessionCard();

  if (isEditing) {
    return (
      <>
        <input
          type="text"
          className="form-control rounded-5 mb-2"
          placeholder="Nome"
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
        />
        <input
          type="text"
          data-cy="description-input"
          className="form-control rounded-5"
          placeholder="Descrizione"
          value={editedDescription}
          onChange={(e) => setEditedDescription(e.target.value)}
        />
      </>
    );
  }

  return (
    <Link href={`/sessions/${session.id}`} className="text-decoration-none text-dark">
      <h4 data-cy="session-title" className="card-title text-primary">{session.title}</h4>
      <p data-cy="session-description" className="card-text">{session.description}</p>
    </Link>
  );
}
