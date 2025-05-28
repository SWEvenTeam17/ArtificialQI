import React from "react";
import { useState } from "react";

export default function PromptCard({ prompt, onDelete, onView, onEdit }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedPrompt, setEditedPrompt] = useState({
    prompt_text: prompt.prompt_text,
    expected_answer: prompt.expected_answer,
  });

  const handleChange = (e) => {
    setEditedPrompt({
      ...editedPrompt,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = () => {
    if (onEdit) {
      onEdit(prompt.id, editedPrompt);
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedPrompt({
      prompt_text: prompt.prompt_text,
      expected_answer: prompt.expected_answer,
    });
    setIsEditing(false);
  };

  return (
    <div className="card shadow-sm h-100 border-primary">
      <div className="card-body">
        <h5 className="card-title">Domanda #{prompt.id}</h5>
        {isEditing ? (
          <>
            <div className="mb-2">
              <strong>Domanda:</strong>
              <input
                type="text"
                className="form-control"
                name="prompt_text"
                value={editedPrompt.prompt_text}
                onChange={handleChange}
              />
            </div>
            <div>
              <strong>Risposta attesa:</strong>
              <input
                type="text"
                className="form-control"
                name="expected_answer"
                value={editedPrompt.expected_answer}
                onChange={handleChange}
              />
            </div>
          </>
        ) : (
          <>
            <p className="card-text">
              <strong>Domanda:</strong> {prompt.prompt_text}
            </p>
            <p className="card-text">
              <strong>Risposta attesa:</strong> {prompt.expected_answer}
            </p>
          </>
        )}
      </div>
      <div className="card-footer text-end">
        <button
          className="btn btn-outline-primary btn-sm me-2"
          onClick={() => onView(prompt.id)}
          disabled={isEditing}
        >
          Visualizza run
        </button>
        {isEditing ? (
          <>
            <button
              className="btn btn-outline-success btn-sm me-2"
              onClick={handleSave}
            >
              Salva
            </button>
            <button
              className="btn btn-outline-success btn-sm me-2"
              onClick={handleCancel}
            >
              Annulla
            </button>
          </>
        ) : (
          <>
            <button
              className="btn btn-outline-success btn-sm me-2"
              onClick={() => setIsEditing(true)}
            >
              Modifica
            </button>
            <button
              className="btn btn-outline-danger btn-sm"
              onClick={() => onDelete(prompt.id)}
            >
              Elimina
            </button>
          </>
        )}
      </div>
    </div>
  );
}
