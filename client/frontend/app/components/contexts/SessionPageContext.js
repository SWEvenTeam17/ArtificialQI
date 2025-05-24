"use client";
import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";

import { getCSRFToken } from "@/app/helpers/csrf";

const TestContext = createContext();

export const useTestContext = () => {
  return useContext(TestContext);
};

export const SessionPageContextProvider = ({ children, sessionId }) => {
  const [sessionData, setSessionData] = useState(null);
  const [remainingLLMs, setRemainingLLMs] = useState(null);
  const [limit, setLimit] = useState(null);
  const [isLLMDataEmpty, setIsLLMDataEmpty] = useState(
    !remainingLLMs || remainingLLMs.length === 0
  );
  useEffect(() => {
    setIsLLMDataEmpty(!remainingLLMs || remainingLLMs.length === 0);
  }, [remainingLLMs]);

  const submitLLM = async (e) => {
    e.preventDefault();

    if (sessionData.llm.length >= 3) {
      setLimit("Solo un massimo di 3 LLM è ammesso.");
    } else {
      const formData = new FormData(e.target);
      const data = {
        sessionId: sessionData.id,
        llmId: formData.get("selectllm"),
      };
      const JSONData = JSON.stringify(data);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_add/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSONData,
        }
      );
      const result = await response.json();
      setSessionData((prevSessionData) => ({
        ...prevSessionData,
        llm: [...prevSessionData.llm, result],
      }));
      fetchRemainingLLMs();
    }
  };

  const fetchSessionData = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${sessionId}`,
        {
          cache: "no-store",
        }
      );
      const data = await response.json();
      setSessionData(data);
    } catch (error) {
      console.error("Error fetching session data:", error);
      setSessionData(null);
    }
  }, [sessionId]);
  const fetchRemainingLLMs = useCallback(async () => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_remaining/${sessionId}`)
      .then((response) => response.json())
      .then((data) => {
        setRemainingLLMs(Array.isArray(data) ? data : []);
      })
      .catch((error) => {
        console.error("Error fetching LLM data:", error);
        setRemainingLLMs([]);
      });
  }, [sessionId]);

  const deleteLLM = async (llmId) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_delete/${sessionId}/${llmId}`,
      {
        method: "DELETE",
        headers: { "X-CSRFToken": getCSRFToken() },
      }
    );
    if (!response.ok) {
      throw new Error(response.statusText);
    }
    if (response.status !== 204) {
      await response.json();
    }
    setSessionData((prevSessionData) => ({
      ...prevSessionData,
      llm: prevSessionData.llm.filter((llm) => llm.id !== llmId),
    }));
    fetchRemainingLLMs();
  };

  useEffect(() => {
    fetchSessionData();
    fetchRemainingLLMs();
  }, [fetchSessionData, fetchRemainingLLMs]);

  const contextValue = useMemo(
    () => ({
      sessionData,
      remainingLLMs,
      limit,
      isLLMDataEmpty,
      setSessionData,
      setRemainingLLMs,
      fetchSessionData,
      fetchRemainingLLMs,
      submitLLM,
      setLimit,
      deleteLLM,
    }),
    [sessionData, remainingLLMs, limit, isLLMDataEmpty]
  );

  return (
    <TestContext.Provider value={contextValue}>{children}</TestContext.Provider>
  );
};
