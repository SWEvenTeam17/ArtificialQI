"use client";
import { getCSRFToken } from "@/app/helpers/csrf";
import delteIcon from "/public/images/icon.png";
import Image from "next/image";

const LLMCard = ({ id, llm, fetchLLMData, setSessionData }) => {
  

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
        >
          <Image width={32} height={32} alt="Elimina llm" src={delteIcon} />
        </button>
      </div>
    </div>
  );
};
export default LLMCard;
