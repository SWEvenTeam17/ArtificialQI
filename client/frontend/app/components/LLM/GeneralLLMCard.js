"use client";
import { getCSRFToken } from "@/app/helpers/csrf";
import delteIcon from "/public/images/icon.png";
import Image from "next/image";

const GeneralLLMCard = ({ llm, fetchLLMList }) => {
  const deleteLLM = async (id) => {
    let data = {
      id: id,
    };
    const JSONData = JSON.stringify(data);
    try {
      await fetch(`http://backend:8000/llm_list/${id}/`, {
        method: "DELETE",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSONData,
      });
      fetchLLMList();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="card shadow-sm border-light rounded-5 h-100 d-flex flex-column">
      <div className="card-body d-flex flex-column justify-content-between">
        <h3 className="card-title text-primary">{llm.name}</h3>
        <p className="card-text text-muted">
          Numero di Parametri: {llm.n_parameters}
        </p>
        <button
          className="btn btn-danger w-100 rounded-5 mt-auto"
          onClick={() => deleteLLM(llm.id)}
        >
          <Image width={32} height={32} alt="Elimina llm" src={delteIcon} />
        </button>
      </div>
    </div>
  );
};
export default GeneralLLMCard;
