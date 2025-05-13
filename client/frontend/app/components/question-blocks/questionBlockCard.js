"use client";
import Link from "next/link";

let QuestionBlockCard = ({ block, onDelete }) => {
  return (
    <div className="card text-center rounded-5 border-light shadow hover-grow p-3 mb-2 w-100">
      <Link
        href={`/question-blocks/${block.id}`}
        className="text-decoration-none text-dark"
      >
        <div className="card-body">
          <h4 className="card-title text-primary">{block.name}</h4>
        </div>
      </Link>
      <div className="card-body">
        <div className="overflow-auto" style={{ maxHeight: '150px', minHeight:'150px' }}>
          {block.prompt && block.prompt.length > 0 ? (
            <ul className="list-unstyled">
              {block.prompt.map((prompt, promptIndex) => {
                return (
                  <li key={promptIndex} className="mb-2">
                    {prompt.prompt_text}
                  </li>
                );
              })}
            </ul>
            
          ) : (
            <p>Nessuna domanda disponibile.</p>
          )}
          
        </div>
        <button className="btn btn-danger rounded-5 w-50" onClick={(e)=>{e.preventDefault(); onDelete(block.id)}}> Elimina blocco</button>
      </div>
    </div>
  );
};

export default QuestionBlockCard;
