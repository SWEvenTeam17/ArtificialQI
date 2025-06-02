import { createContext, useContext, useState } from "react";
import { useSessionContext } from "./SessionContext";

const SessionCardContext = createContext();

export function SessionCardProvider({ session, children }) {
  const { updateSession, deleteSession } = useSessionContext();
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(session.title);
  const [editedDescription, setEditedDescription] = useState(
    session.description,
  );

  const startEditing = () => setIsEditing(true);
  const cancelEditing = () => {
    setIsEditing(false);
    setEditedTitle(session.title);
    setEditedDescription(session.description);
  };

  const saveChanges = () => {
    updateSession(session.id, {
      title: editedTitle,
      description: editedDescription,
    });
    setEditedTitle(editedTitle);
    setEditedDescription(editedDescription);
    setIsEditing(false);
  };

  const removeSession = () => deleteSession(session.id);

  return (
    <SessionCardContext.Provider
      value={{
        session,
        isEditing,
        editedTitle,
        editedDescription,
        setEditedTitle,
        setEditedDescription,
        startEditing,
        cancelEditing,
        saveChanges,
        removeSession,
      }}
    >
      {children}
    </SessionCardContext.Provider>
  );
}

export function useSessionCard() {
  const context = useContext(SessionCardContext);
  if (!context) {
    throw new Error(
      "useSessionCard deve essere usato dentro un <SessionCardProvider>",
    );
  }
  return context;
}
