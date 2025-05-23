import React, { useState, useCallback, useEffect } from "react";
import TestFormPresentational from "../../presentations/sessions/TestFormPresentational";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function TestFormContainer({ sessionData }) {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null);
  const [selectedBlocks, setSelectedBlocks] = useState([]);
  const [error, setError] = useState(null); // 🔴 Nuovo stato per l'errore

  const addBlock = async (id) => {
    try {
      let response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`);
      if (!response.ok) throw new Error("Errore nel recupero del blocco");
      let data = await response.json();
      setSelectedBlocks((prevBlocks) => [...prevBlocks, data]);
      setError(null);
    } catch (err) {
      setError("Errore durante l'aggiunta del blocco.");
    }
  };

  const removeBlock = (id) => {
    setSelectedBlocks((prevBlocks) => prevBlocks.filter((block) => block.id !== id));
    setError(null);
  };

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      let response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`);
      if (!response.ok) throw new Error("Errore nel recupero dei blocchi");
      let data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0
      );
      setQuestionBlocks(filteredData);
      setError(null);
    } catch (error) {
      console.error("Errore durante il recupero dei blocchi di domande:", error);
      setError("Impossibile caricare i blocchi di domande.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, [fetchQuestionBlocks]);

  const isSelected = (questionId) => {
    return selectedBlocks.some((q) => q.id === questionId);
  };

  const submitToBackend = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          sessionId: sessionData.id,
          blocks: selectedBlocks,
        }),
      });
      const data = await response.json();
      setTestResults(data);
      setActiveView("results");
      setError(null);
    } catch (error) {
      console.error("Errore durante l'esecuzione del test:", error);
      setError("Errore durante l'esecuzione del test:", error);
    } finally {
      setLoading(false);
    }
  };

  const showPrevTests = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/`
      );
      if (!response.ok) throw new Error("Errore nel recupero dei test precedenti");
      const data = await response.json();
      setPrevTests(data);
      setActiveView("prev");
      setError(null);
    } catch (error) {
      console.error("Errore nel recupero dei test precedenti:", error);
      setError("Errore nel recupero dei test precedenti.");
    }
  };

  const handlePrevTestClick = async (test) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`
      );
      if (!response.ok) throw new Error("Errore nel recupero del test selezionato");
      const data = await response.json();
      setTestResults(data);
      setActiveView("results");
      setError(null);
    } catch (error) {
      console.error("Errore caricando il test precedente:", error);
      setError("Errore caricando il test precedente.");
    }
  };

  return (
    <TestFormPresentational
      selectedBlocks={selectedBlocks}
      testResults={testResults}
      loading={loading}
      questionBlocks={questionBlocks}
      isSelected={isSelected}
      removeBlock={removeBlock}
      addBlock={addBlock}
      submitToBackend={submitToBackend}
      prevTests={prevTests}
      setPrevTests={setPrevTests}
      activeView={activeView}
      showPrevTests={showPrevTests}
      handlePrevTestClick={handlePrevTestClick}
      error={error} // 🔴 Passa l'errore al presentazionale
    />
  );
}
