import React from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
import GeneralLLMCardPresentational from "../../presentations/LLM-Manager/GeneralLLMCardPresentational";

export default function GeneralLLMCardContainer({llm, fetchLLMList}) {
  const deleteLLM = async (id) => {
    let data = {
      id: id,
    };
    const JSONData = JSON.stringify(data);
    try {
      await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/${id}/`, {
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
  return(<GeneralLLMCardPresentational deleteLLM={deleteLLM} llm={llm}/>)
}
