import React from "react";

export default function PromptCard({ prompt, onDelete, onView }) {
  return (
    <div className="card shadow-sm h-100 border-primary">
      <div className="card-body">
        <h5 className="card-title">Domanda #{prompt.id}</h5>
        <p className="card-text">
          <strong>Domanda:</strong> {prompt.prompt_text}
        </p>
        <p className="card-text">
          <strong>Risposta attesa:</strong> {prompt.expected_answer}
        </p>
      </div>
      <div className="card-footer text-end">
        <button
          className="btn btn-outline-primary btn-sm me-2"
          onClick={() => onView(prompt.id)}
        >
          Visualizza run
        </button>
        <button
          className="btn btn-outline-danger btn-sm"
          onClick={() => onDelete(prompt.id)}
        >
          Elimina prompt
        </button>
      </div>
    </div>
  );
}
