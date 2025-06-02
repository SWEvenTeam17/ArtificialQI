import Link from "next/link";

export default function QuestionBlockCard({ block, onDelete }) {
  return (
    <div className="card text-center rounded-5 border-light shadow hover-grow p-3 mb-2 w-100">
      <Link
        href={`/question-blocks/${block.id}`}
        className="text-decoration-none text-dark"
      >
        <div className="card-body">
          <h4 className="card-title text-primary">{block.name}</h4>

          <div
            className="overflow-auto"
            style={{ maxHeight: "150px", minHeight: "150px" }}
          >
            {block.prompt && block.prompt.length > 0 ? (
              <ul className="list-group list-group-flush">
                {block.prompt.map((prompt, promptIndex) => (
                  <li key={promptIndex} className="list-group-item">
                    Domanda: {prompt.prompt_text} Risposta attesa:{" "}
                    {prompt.expected_answer}
                  </li>
                ))}
              </ul>
            ) : (
              <p>Nessuna domanda disponibile.</p>
            )}
          </div>
        </div>
      </Link>

      <div className="card-body">
        <button
          className="btn btn-danger rounded-5 w-50 mt-2"
          onClick={(e) => {
            e.preventDefault();
            onDelete(block.id);
          }}
        >
          Elimina blocco
        </button>
      </div>
    </div>
  );
}
