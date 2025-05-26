"use client";
import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from "react";
import { getCSRFToken } from "@/app/helpers/csrf";

const QuestionBlockContext = createContext();

export function QuestionBlockProvider({ children }) {
  const [questionBlocks, setQuestionBlocks] = useState([]);

  const addQuestionBlock = useCallback((newBlock) => {
    setQuestionBlocks((prev) => [...prev, newBlock]);
  }, []);

  const fetchQuestionBlocks = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
      );
      const data = await response.json();
      setQuestionBlocks(data);
    } catch (error) {
      console.error("Errore nel fetch dei blocchi:", error);
    }
  }, []);

  const deleteQuestionBlock = useCallback(async (id) => {
    try {
      await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`,
        {
          method: "DELETE",
          headers: {
            "X-CSRFToken": getCSRFToken(),
          },
        }
      );
      setQuestionBlocks((prev) => prev.filter((block) => block.id !== id));
    } catch (error) {
      console.error("Errore durante l'eliminazione:", error);
    }
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, [fetchQuestionBlocks]);

  return (
    <QuestionBlockContext.Provider
      value={{ questionBlocks, deleteQuestionBlock, addQuestionBlock }}
    >
      {children}
    </QuestionBlockContext.Provider>
  );
}

export function useQuestionBlockContext() {
  return useContext(QuestionBlockContext);
}
