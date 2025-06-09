import {
  useState,
  useEffect,
  useCallback,
  createContext,
  useContext,
} from "react";

const InspectBlockContext = createContext();

export function useInspectBlockContext() {
  return useContext(InspectBlockContext);
}

export function InspectBlockProvider({ children, id }) {
  const [blockData, setBlockData] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [uniqueId, setUniqueId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBlockData = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}`,
      );
      if (!response.ok) throw new Error("Errore nel recupero dell'insieme di domande.");
      const parsed = await response.json();
      setBlockData(parsed);
    } catch (err) {
      setError(err.message || "Errore sconosciuto");
    } finally {
      setLoading(false);
    }
  }, [id]);

  const deletePrompt = async (promptId) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_list/${promptId}/`,
        {
          method: "DELETE",
        },
      );

      if (response.status === 204) {
        const updatedPrompts = blockData.prompt.filter(
          (prompt) => prompt.id !== promptId,
        );
        setBlockData({ ...blockData, prompt: updatedPrompts });
      } else {
        console.error("Errore nella cancellazione del prompt");
      }
    } catch (err) {
      console.error("Errore nella richiesta:", err);
    }
  };

  const handleView = async (promptId) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_runs/?prompt_id=${promptId}`,
    );
    const data = await response.json();
    setUniqueId(promptId);
    setTestResults(data);
  };

  const handleEdit = async (promptId, editedPrompt) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_list/${promptId}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(editedPrompt),
        },
      );
      if (!response.ok)
        throw new Error("Errore durante la modifica del prompt.");
      const updated = await response.json();

      setBlockData((prev) => ({
        ...prev,
        prompt: prev.prompt.map((p) =>
          p.id === promptId ? { ...p, ...updated } : p,
        ),
      }));
    } catch (err) {
      setError(err);
    }
  };

  useEffect(() => {
    fetchBlockData();
  }, [id, fetchBlockData]);

  return (
    <InspectBlockContext.Provider
      value={{
        blockData,
        testResults,
        uniqueId,
        loading,
        error,
        deletePrompt,
        handleView,
        handleEdit,
      }}
    >
      {children}
    </InspectBlockContext.Provider>
  );
}
