import React from "react";
import { useState, useEffect } from "react";
import LLMManagerPresentational from "../../presentations/LLM-Manager/LLMManagerPresentational";
export const LLMManagerContainer = () => {
  const [LLMList, setLLMList] = useState([]);

  useEffect(() => {
    fetchLLMList();
  }, []);

  const fetchLLMList = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`
      );
      const data = await response.json();
      setLLMList(data);
    } catch (error) {
      console.error("Error fetching LLM list:", error);
    }
  };
  return (
    <LLMManagerPresentational fetchLLMList={fetchLLMList} LLMList={LLMList}/>
  );
};
