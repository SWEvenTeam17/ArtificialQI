import React from "react";
import { useState, useEffect } from "react";
import InspectBlockPagePresentational from "../../presentations/question-blocks/InspectBlockPagePresentational";

export default function InspectBlockPageContainer({ id }) {
  const [blockData, setBlockData] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [uniqueId, setUniqueId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBlockData = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}`
      );
      if (!response.ok) throw new Error("Errore nel recupero del blocco");
      const parsed = await response.json();
      setBlockData(parsed);
    } catch (err) {
      setError(err.message || "Errore sconosciuto");
    } finally {
      setLoading(false);
    }
  };

  const deletePrompt = async (promptId) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_list/${promptId}/`,
        {
          method: "DELETE",
        }
      );

      if (response.status === 204) {
        const updatedPrompts = blockData.prompt.filter(
          (prompt) => prompt.id !== promptId
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
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_runs?prompt_id=${promptId}`
    );
    const data = await response.json();
    setUniqueId(promptId);
    setTestResults(data);
  };

  useEffect(() => {
    fetchBlockData();
  }, []);

  return (
    <InspectBlockPagePresentational
      blockData={blockData}
      loading={loading}
      error={error}
      deletePrompt={deletePrompt}
      handleView={handleView}
      testResults={testResults}
      uniqueId={uniqueId}
    />
  );
}
