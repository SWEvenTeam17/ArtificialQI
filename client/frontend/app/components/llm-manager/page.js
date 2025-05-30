"use client";

import { useState, useEffect, useMemo, useCallback } from "react";
import LLMManager from "../llm-manager/LLMManager";
import { LLMManagerContext } from "../../../app/components/contexts/LLMManagerContext";



export default function Page() {
  const [LLMList, setLLMList] = useState([]);

  const fetchLLMList = useCallback(async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`);
      const data = await res.json();
      setLLMList(data);
    } catch (err) {
      console.error("Failed to fetch LLMs", err);
    }
  }, []);

  const deleteLLM = useCallback(async (id) => {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/${id}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
      fetchLLMList();
    } catch (err) {
      console.error("Failed to delete LLM", err);
    }
  }, [fetchLLMList]);

  useEffect(() => {
    fetchLLMList();
  }, [fetchLLMList]);

  const value = useMemo(() => ({
    LLMList,
    fetchLLMList,
    deleteLLM,
  }), [LLMList, fetchLLMList, deleteLLM]);

  return (
    <LLMManagerContext.Provider value={value}>
      <LLMManager />
    </LLMManagerContext.Provider>
  );
}


