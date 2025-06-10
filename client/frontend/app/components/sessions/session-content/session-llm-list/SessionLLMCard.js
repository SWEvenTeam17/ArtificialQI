import delteIcon from "/public/images/icon.png";
import Image from "next/image";
export default function SessionLLMCard({ llm, deleteLLM }) {
  return (
    <div className="card rounded-5">
      <div className="card-body">
        <h5 className="card-title text-primary">{llm.name}</h5>
        <p className="card-text text-muted">
          Numero di Parametri: {llm.n_parameters}
        </p>
        <button
          className="btn btn-danger w-50 rounded-5"
          onClick={() => deleteLLM(llm.id)}
          data-cy={`delete-llm-button`}
        >
          <Image width={32} height={32} alt="Elimina llm" src={delteIcon} />
        </button>
      </div>
    </div>
  );
}
