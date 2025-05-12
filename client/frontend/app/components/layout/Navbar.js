"use client";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function Navbar({ sessions, fetchSessions }) {
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
    <nav className="navbar bg-body-tertiary">
      <div className="container-fluid justify-content-start">
        <button
          className="navbar-toggler me-2"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#offcanvasNavbar"
          aria-controls="offcanvasNavbar"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <Link className="navbar-brand" href="/">
          ArtificialQI
        </Link>
        <ul className="navbar-nav flex-row me-auto mb-2 mb-lg-0">
          <li className="nav-item me-3">
            <Link className="nav-link" href="/">
              Home
            </Link>
          </li>
          <li className="nav-item me-3">
            <Link className="nav-link" href="/manage-llm">
              Gestisci LLM
            </Link>
          </li>
          <li className="nav-item me-3">
            <Link className="nav-link" href="/compare">
              Confronta risultati
            </Link>
          </li>
        </ul>
        <div
          className="offcanvas offcanvas-start"
          tabIndex="-1"
          id="offcanvasNavbar"
          aria-labelledby="offcanvasNavbarLabel"
        >
          <div className="offcanvas-header">
            <h1 className="offcanvas-title" id="offcanvasNavbarLabel">
              ArtificialQI
            </h1>
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="offcanvas"
              aria-label="Close"
            ></button>
          </div>
          <div className="offcanvas-body">
            <AccordionForm
              {...{
                onSubmit,
                formErrors,
                title,
                setTitle,
                description,
                setDescription,
              }}
            />
            <div className="mt-4">
              <ul className="list-group">
                {sessions.map((session) => (
                  <NavbarSessionElement
                    session={session}
                    key={session.id}
                  ></NavbarSessionElement>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavbarSessionElement({ session }) {
  const router = useRouter();
  return (
    <Link
      href={`/sessions/${session.id}`}
      onClick={() => router.push(`/sessions/${session.id}`)}
      data-bs-dismiss="offcanvas"
      className="btn w-100 mt-2 btn-light rounded-5 border"
    >
      {session.title}
    </Link>
  );
}

function AccordionForm({
  onSubmit,
  formErrors,
  title,
  setTitle,
  description,
  setDescription,
}) {
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
            <div className="container align-items-center">
              <div className="mt-3">
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
                  <div className="text-center align-items-center col-12">
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
      </div>
    </div>
  );
}
