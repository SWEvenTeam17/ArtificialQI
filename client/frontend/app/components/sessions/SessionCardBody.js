import Link from "next/link";
import { useSessionCard } from "@/app/components/contexts/session/SessionCardContext";
import { useEffect, useState } from "react";

export default function SessionCardBody() {
  const {
    session,
    isEditing,
    editedTitle,
    editedDescription,
    setEditedTitle,
    setEditedDescription,
  } = useSessionCard();

  const [lastClicked, setLastClicked] = useState(null);

  useEffect(() => {
    if (session?.id) {
      const stored = localStorage.getItem(`session_last_clicked_${session.id}`);
      if (stored) setLastClicked(new Date(stored));
    }
  }, [session?.id]);

  const handleCardClick = () => {
    const now = new Date();
    localStorage.setItem(
      `session_last_clicked_${session.id}`,
      now.toISOString(),
    );
    setLastClicked(now);
  };

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
          className="form-control rounded-5"
          placeholder="Descrizione"
          data-cy="description-input"
          value={editedDescription}
          onChange={(e) => setEditedDescription(e.target.value)}
        />
      </>
    );
  }

  return (
    <Link
      href={`/sessions/${session.id}`}
      className="text-decoration-none text-dark"
      onClick={handleCardClick}
    >
      <h4 className="card-title text-primary" data-cy="session-title">
        {session.title}
      </h4>
      <p className="card-text">{session.description}</p>
      <small className="text-muted">
        Ultimo accesso:{" "}
        {lastClicked
          ? lastClicked.toLocaleString("it-IT", {
              day: "2-digit",
              month: "2-digit",
              year: "numeric",
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
              hour12: false,
            })
          : "Mai"}
      </small>
    </Link>
  );
}
