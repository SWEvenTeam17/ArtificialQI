"use client";
import { useRouter } from "next/navigation";
import SessionCardPresentational from "../../presentations/sessions/SessionCardPresentational";
import { useState } from "react";
import { useSessionContext } from "../../contexts/SessionContext";
export default function SessionCardContainer({ session }) {
  const { updateSession, deleteSession } = useSessionContext();
  const router = useRouter();
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(session.title);
  const [editedDescription, setEditedDescription] = useState(
    session.description,
  );

  const handleSave = () => {
    updateSession(session.id, {
      title: editedTitle,
      description: editedDescription,
    });
    setIsEditing(false);
  };

  return (
    <SessionCardPresentational
      handleSave={handleSave}
      session={session}
      deleteSession={deleteSession}
      editedDescription={editedDescription}
      editedTitle={editedTitle}
      isEditing={isEditing}
      setIsEditing={setIsEditing}
      setEditedTitle={setEditedTitle}
      setEditedDescription={setEditedDescription}
    />
  );
}
