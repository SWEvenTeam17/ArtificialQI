"use client";
import { useState } from "react";
import { useSessionContext } from "@/app/components/contexts/session/SessionContext";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function AccordionForm() {
  const { sessions, fetchSessions } = useSessionContext();

  const [formErrors, setFormErrors] = useState({});
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const validateForm = () => {
    const errors = {};
    if (!title) errors.title = "Il titolo è obbligatorio.";
    if (!description) errors.description = "La descrizione è obbligatoria.";
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

    try {
      await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/`, {
        method: "POST",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify(data),
      });

      fetchSessions();
      event.target.reset();
      setTitle("");
      setDescription("");
    } catch (error) {
      console.error("Errore nella creazione della sessione:", error);
    }
  };

  return (
    <div className="accordion" id="formAccordion">
      <div className="accordion-item">
        <h2 className="accordion-header" id="headingForm">
          <button
            className="accordion-button"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseForm"
            aria-expanded="true"
            aria-controls="collapseForm"
          >
            Crea nuova sessione
          </button>
        </h2>
        <div
          id="collapseForm"
          className="accordion-collapse collapse show"
          aria-labelledby="headingForm"
          data-bs-parent="#formAccordion"
        >
          <div className="accordion-body">
            <form onSubmit={onSubmit}>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className={`form-control rounded-5 ${formErrors.title ? "is-invalid" : ""}`}
                  id="title"
                  name="title"
                  placeholder="Titolo"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                />
                <label htmlFor="title">Titolo</label>
                {formErrors.title && (
                  <div className="invalid-feedback">{formErrors.title}</div>
                )}
              </div>
              <div className="form-floating mb-3">
                <input
                  type="text"
                  className={`form-control rounded-5 ${formErrors.description ? "is-invalid" : ""}`}
                  id="description"
                  name="description"
                  placeholder="Descrizione"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
                <label htmlFor="description">Descrizione</label>
                {formErrors.description && (
                  <div className="invalid-feedback">
                    {formErrors.description}
                  </div>
                )}
              </div>
              <div className="text-center">
                <button
                  type="submit"
                  className="btn btn-primary w-50 rounded-5"
                >
                  Crea
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
