import { useSessionContext } from "@/app/components/contexts/SessionContext";
import { useState } from "react";
import NavbarPresentational from "@/app/components/presentations/layout/navbar/NavbarPresentational";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function NavbarContainer() {
  const { sessions, fetchSessions } = useSessionContext();
  const [formErrors, setFormErrors] = useState({});
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const validateForm = () => {
    const errors = {};

    if (!title) {
      errors.title = "Il titolo è obbligatorio.";
    }

    if (!description) {
      errors.description = "La descrizione è obbligatoria.";
    }

    return errors;
  };

  const onSubmit = async (event) => {
    event.preventDefault();

    const errors = validateForm();
    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    const isDuplicate = sessions.some((session) => session.title === title);
    if (isDuplicate) {
      setFormErrors({ title: "Esiste già una sessione con questo titolo." });
      return;
    }

    setFormErrors({});

    const formData = new FormData(event.target);
    const data = {
      title: formData.get("title"),
      description: formData.get("description"),
    };

    const JSONData = JSON.stringify(data);

    try {
      await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/`, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSONData,
      });

      fetchSessions();
      event.target.reset();
      setTitle("");
      setDescription("");
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  };

  return (
    <>
      <NavbarPresentational
        sessions={sessions}
        onSubmit={onSubmit}
        formErrors={formErrors}
        title={title}
        setTitle={setTitle}
        description={description}
        setDescription={setDescription}
      />
    </>
  );
}
