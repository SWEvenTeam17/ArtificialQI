import React, { act } from "react";
import TestFormPresentational from "../../presentations/sessions/TestFormPresentational";
import { useState, useCallback, useEffect } from "react";
import { useBlocksContext } from "../../contexts/BlocksContext";
import { getCSRFToken } from "@/app/helpers/csrf";

export default function TestFormContainer({ sessionData }) {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const { selectedBlocks, addBlock, removeBlock } = useBlocksContext();
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null); // null | "prev" | "results"

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
      );
      let data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0
      );
      setQuestionBlocks(filteredData);
    } catch (error) {
      console.error(
        "Errore durante il recupero dei blocchi di domande:",
        error
      );
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
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify({
            sessionId: sessionData.id,
            blocks: selectedBlocks,
          }),
        }
      );
      const data = await response.json();
      setActiveView("results");
      setTestResults(data);
    } catch (error) {
      console.error("Errore durante l'esecuzione del test:", error);
    } finally {
      setLoading(false);
    }
  };

  const showPrevTests = async () => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/`
    );
    const data = await response.json();
    setPrevTests(data);
    setActiveView("prev");
  };

  const handlePrevTestClick = async (test) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`
    );
    const data = await response.json();
    console.log(data);
    setTestResults(data);
    setActiveView("results");
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
    />
  );
}
