import {
  useState,
  useEffect,
  useMemo,
  useCallback,
  useContext,
  createContext,
} from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
const LLMManagerContext = createContext();

export function useLLMManagerContext() {
  return useContext(LLMManagerContext);
}

export function LLMManagerContextProvider({ children }) {
  const [LLMList, setLLMList] = useState([]);

  const fetchLLMList = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`,
      );
      const data = await response.json();
      setLLMList(data);
    } catch (error) {
      console.error("Error fetching LLM list:", error);
    }
  }, []);

  const deleteLLM = useCallback(
    async (id) => {
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
    },
    [fetchLLMList],
  );

  useEffect(() => {
    fetchLLMList();
  }, [fetchLLMList]);

  const value = useMemo(
    () => ({
      LLMList,
      fetchLLMList,
      deleteLLM,
    }),
    [LLMList, fetchLLMList, deleteLLM],
  );

  return (
    <LLMManagerContext.Provider value={value}>
      {children}
    </LLMManagerContext.Provider>
  );
}
