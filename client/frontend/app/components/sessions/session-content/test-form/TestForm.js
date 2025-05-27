import { useState, useCallback, useEffect } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
import TestResults from "../TestResults";
import PrevTests from "../../../results/PrevTests";
import JSONView from "./JSONView";
import JSONSelector from "./JSONSelector";
import TestActions from "./TestActions";
import QuestionBlocksSelector from "./QuestionBlocksSelector";
import { useTestContext } from "@/app/components/contexts/TestContext";
export default function TestForm() {
  const { sessionData } = useTestContext();
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const [testResults, setTestResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prevTests, setPrevTests] = useState([]);
  const [activeView, setActiveView] = useState(null);
  const [selectedBlocks, setSelectedBlocks] = useState([]);
  const [isJSON, setIsJSON] = useState(false);
  const [jsonFile, setJsonFile] = useState(null);
  const [error, setError] = useState(null);

  const addBlock = async (id) => {
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`
      );
      if (!response.ok) throw new Error("Errore nel recupero del blocco");
      let data = await response.json();
      setSelectedBlocks((prevBlocks) => [...prevBlocks, data]);
      setError(null);
    } catch (err) {
      setError("Errore durante l'aggiunta del blocco.");
    }
  };

  const removeBlock = (id) => {
    setSelectedBlocks((prevBlocks) =>
      prevBlocks.filter((block) => block.id !== id)
    );
    setError(null);
  };

  const fetchQuestionBlocks = useCallback(async () => {
    setLoading(true);
    try {
      let response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
      );
      if (!response.ok) throw new Error("Errore nel recupero dei blocchi");
      let data = await response.json();
      const filteredData = data.filter(
        (block) => Array.isArray(block.prompt) && block.prompt.length > 0
      );
      setQuestionBlocks(filteredData);
      setError(null);
    } catch (error) {
      console.error(
        "Errore durante il recupero dei blocchi di domande:",
        error
      );
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
  };

  const handlePrevTestClick = async (test) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${sessionData.id}/?test_id=${test.id}`
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
  };

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
                  typeof p.answer === "string"
              )
          );
          if (valid) {
            setSelectedBlocks(blocks);
            setError(null);
          } else {
            setError("Il file JSON non ha il formato corretto.");
          }
        } catch (err) {
          setError("Errore durante la lettura del file JSON.");
        }
      };
      reader.readAsText(file);
      setJsonFile(file);
    } else {
      setError("Inserisci un file JSON valido.");
    }
  };

  const handleJSONSubmit = async (e) => {
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
            }
          );
          if (!response.ok)
            throw new Error("Errore nella creazione del blocco da JSON.");
          return await response.json();
        })
      );
      setError(null);
      setIsJSON(false);
      await fetchQuestionBlocks();

      setQuestionBlocks((prevBlocks) => {
        const names = createdBlocks.map((b) => b.name);
        const selected = prevBlocks.filter((b) => names.includes(b.name));
        setSelectedBlocks(selected);
        return prevBlocks;
      });
    } catch (err) {
      setError("Errore durante la creazione dei blocchi da JSON.");
    }
  };

  return (
    <>
      <div className="card border-0">
        <div className="card-body">
          <JSONSelector
            isJSON={isJSON}
            setIsJSON={setIsJSON}
            setSelectedBlocks={setSelectedBlocks}
          />
        </div>
      </div>

      {isJSON && (
        <JSONView
          handleJSONSubmit={handleJSONSubmit}
          handleJSONFileChange={handleJSONFileChange}
          loading={loading}
        />
      )}

      {error && (
        <div className="alert alert-danger text-center" role="alert">
          {error}
        </div>
      )}

      {!isJSON && questionBlocks.length > 0 && (
        <QuestionBlocksSelector
          questionBlocks={questionBlocks}
          isSelected={isSelected}
          removeBlock={removeBlock}
          addBlock={addBlock}
        />
      )}

      {!isJSON && questionBlocks.length === 0 && (
        <p className="text-center fs-3">
          È necessario creare dei blocchi di domande per eseguire un test.
        </p>
      )}
      <TestActions
        submitToBackend={submitToBackend}
        selectedBlocks={selectedBlocks}
        showPrevTests={showPrevTests}
        loading={loading}
      />
      {testResults && activeView === "results" && (
        <div className="card mt-4">
          <div className="card-body">
            <TestResults testResults={testResults} />
          </div>
        </div>
      )}
      {activeView === "prev" && (
        <div className="mt-4">
          <PrevTests
            prevTests={prevTests}
            setPrevTests={setPrevTests}
            onTestClick={handlePrevTestClick}
          />
        </div>
      )}
    </>
  );
}


