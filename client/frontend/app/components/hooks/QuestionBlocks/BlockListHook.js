import { useState, useEffect, useCallback } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function BlockListHook() {
  const [questionBlocks, setQuestionBlocks] = useState([]);

  const fetchQuestionBlocks = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
      );
      const data = await response.json();
      setQuestionBlocks(data);
    } catch (error) {
      console.error("Errore nel fetch dei blocchi di domande:", error);
    }
  }, []);

  const deleteQuestionBlock = useCallback(async (id) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`,
        {
          method: "DELETE",
          headers: {
            "X-CSRFToken": getCSRFToken(),
          },
        }
      );
      if (response.status === 204) {
        setQuestionBlocks((prev) => prev.filter((block) => block.id !== id));
      }
    } catch (error) {
      console.error("Errore durante l'eliminazione del blocco:", error);
    }
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, [fetchQuestionBlocks]);

  return {
    questionBlocks,
    deleteQuestionBlock,
  };
}
