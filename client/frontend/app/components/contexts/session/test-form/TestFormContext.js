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

const TestFormContext = createContext();
export const useTestFormContext = () => useContext(TestFormContext);

export const TestFormContextProvider = ({ children, sessionData }) => {
  const [selectedBlocks, setSelectedBlocks] = useState([]);
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [testResults, setTestResults] = useState(null);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null);
  const [isJSON, setIsJSON] = useState(false);
  const [jsonFile, setJsonFile] = useState(null);

  const isSelected = useCallback(
    (questionId) => selectedBlocks.some((q) => q.id === questionId),
    [selectedBlocks],
  );

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`,
      );
      if (!response.ok) throw new Error("Errore nel recupero degli insiemi");
      const data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0,
      );
      setQuestionBlocks(filteredData);
      setError(null);
    } catch (error) {
      console.error("Errore durante il recupero degli insiemi:", error);
      setError("Impossibile caricare gli insiemi di domande.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, [fetchQuestionBlocks]);

  const addBlock = useCallback(
    async (id) => {
      try {
        const block = questionBlocks.find((block) => block.id === id);
        if (!block) throw new Error("Blocco non trovato");
        setSelectedBlocks((prev) => [...prev, block]);
        setError(null);
      } catch {
        setError("Errore durante l'aggiunta dell'insieme di domande.");
      }
    },
    [questionBlocks],
  );

  const removeBlock = useCallback((id) => {
    setSelectedBlocks((prev) => prev.filter((block) => block.id !== id));
    setError(null);
  }, []);

  const submitToBackend = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest/`,
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
        },
      );
      const data = await response.json();
      setTestResults(data);
      setActiveView("results");
      setError(null);
    } catch (error) {
      console.error("Errore durante l'esecuzione del test:", error);
      setError("Errore durante l'esecuzione del test.");
    } finally {
      setLoading(false);
    }
  }, [selectedBlocks, sessionData?.id]);

  const showPrevTests = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/`,
      );
      if (!response.ok)
        throw new Error("Errore nel recupero dei test precedenti");
      const data = await response.json();
      setPrevTests(data);
      setActiveView("prev");
      setError(null);
    } catch (error) {
      console.error("Errore nel recupero dei test precedenti:", error);
      setError("Errore nel recupero dei test precedenti.");
    }
  }, [sessionData?.id]);

  const handlePrevTestClick = useCallback(
    async (test) => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`,
        );
        if (!response.ok)
          throw new Error("Errore nel recupero del test selezionato");
        const data = await response.json();
        setTestResults(data);
        setActiveView("results");
        setError(null);
      } catch (error) {
        console.error("Errore caricando il test precedente:", error);
        setError("Errore caricando il test precedente.");
      }
    },
    [sessionData?.id],
  );

  const handleJSONFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const parsed = JSON.parse(event.target.result);
          const blocks = Array.isArray(parsed) ? parsed : [parsed];
          const valid = blocks.every(
            (block) =>
              block &&
              typeof block === "object" &&
              typeof block.name === "string" &&
              Array.isArray(block.questions) &&
              block.questions.every(
                (p) =>
                  typeof p === "object" &&
                  typeof p.question === "string" &&
                  typeof p.answer === "string",
              ),
          );
          if (valid) {
            setSelectedBlocks(blocks);
            setError(null);
          } else {
            setError("Il file JSON non ha il formato corretto.");
          }
        } catch {
          setError("Errore durante la lettura del file JSON.");
        }
      };
      reader.readAsText(file);
      setJsonFile(file);
    } else {
      setError("Inserisci un file JSON valido.");
    }
  };

  const handleJSONSubmit = useCallback(
    async (e) => {
      e.preventDefault();
      if (!jsonFile) {
        setError("Carica un file JSON valido prima di inviare.");
        return;
      }
      try {
        const createdBlocks = await Promise.all(
          selectedBlocks.map(async (block) => {
            const response = await fetch(
              `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`,
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": getCSRFToken(),
                },
                body: JSON.stringify(block),
              },
            );
            if (!response.ok)
              throw new Error(
                "Errore nella creazione dell'insieme di domande da JSON.",
              );
            return await response.json();
          }),
        );
        setIsJSON(false);
        setError(null);
        await fetchQuestionBlocks();

        setQuestionBlocks((prev) => {
          const names = createdBlocks.map((b) => b.name);
          const selected = prev.filter((b) => names.includes(b.name));
          setSelectedBlocks(selected);
          return prev;
        });
      } catch {
        setError("Errore durante la creazione dei blocchi da JSON.");
      }
    },
    [
      selectedBlocks,
      jsonFile,
      setError,
      setIsJSON,
      fetchQuestionBlocks,
      setQuestionBlocks,
      setSelectedBlocks,
    ],
  );

  const value = useMemo(
    () => ({
      selectedBlocks,
      setSelectedBlocks,
      addBlock,
      removeBlock,
      questionBlocks,
      setQuestionBlocks,
      fetchQuestionBlocks,
      isSelected,
      loading,
      error,
      setError,
      testResults,
      setTestResults,
      prevTests,
      setPrevTests,
      activeView,
      setActiveView,
      isJSON,
      setIsJSON,
      jsonFile,
      setJsonFile,
      handleJSONFileChange,
      handleJSONSubmit,
      submitToBackend,
      showPrevTests,
      handlePrevTestClick,
    }),
    [
      selectedBlocks,
      questionBlocks,
      loading,
      error,
      testResults,
      prevTests,
      activeView,
      isJSON,
      jsonFile,
      fetchQuestionBlocks,
      isSelected,
      addBlock,
      handleJSONSubmit,
      handlePrevTestClick,
      removeBlock,
      showPrevTests,
      submitToBackend,
    ],
  );

  return (
    <TestFormContext.Provider value={value}>
      {children}
    </TestFormContext.Provider>
  );
};
