"use client";
import { use, useState, useEffect, useContext, useCallback } from "react";
import { SessionContext } from "@/app/components/contexts/SessionContext";
import AddLLMForm from "@/app/components/LLM/AddLLMForm";
import LLMCard from "@/app/components/LLM/LLMCard";
import { BlocksContextProvider } from "@/app/components/contexts/BlocksContext";
import TestForm from "@/app/components/question-blocks/TestForm";

export default function SessionPage({ params }) {
  const { id } = use(params);
  const { sessions } = useContext(SessionContext);
  const [sessionData, setSessionData] = useState(null);
  const [LLMData, setLLMData] = useState(null);

  const fetchSessionData = useCallback(async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}`,
        {
          cache: "no-store",
        },
      );
      const data = await response.json();
      setSessionData(data);
    } catch (error) {
      console.error("Error fetching session data:", error);
      setSessionData(null);
    }
  }, [id]);
  const fetchLLMData = useCallback(async () => {
    fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_remaining/${id}`)
      .then((response) => response.json())
      .then((data) => {
        setLLMData(Array.isArray(data) ? data : []);
      })
      .catch((error) => {
        console.error("Error fetching LLM data:", error);
        setLLMData([]);
      });
  }, [id]);

  useEffect(() => {
    fetchSessionData();
    fetchLLMData();
  }, [id, fetchSessionData, fetchLLMData]);

  if (sessionData === null) {
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ height: "100vh", backgroundColor: "#f8f9fa" }}
      >
        <div
          className="spinner-grow text-secondary"
          style={{ width: "6rem", height: "6rem" }}
          role="status"
        >
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid">
      <h1 className="text-center mt-3">
        Benvenuto alla sessione
        <span className="text-primary">{" " + sessionData.title}</span>
      </h1>

      <div className="row g-0 p-0 m-0">
        <div className="col-12">
          <div className="card border-0 h-100">
            <div className="card-body text-center">
              <h5 className="card-title text-center text-primary font-weight-bold">
                Gestisci LLM collegati
              </h5>
              <div className="row justify-content-center">
                <div className="col-md-6 col-12">
                  <AddLLMForm
                    LLMData={LLMData}
                    sessionData={sessionData}
                    setSessionData={setSessionData}
                    fetchLLMData={fetchLLMData}
                  />
                </div>
              </div>
              {sessionData.llm.length > 0 ? (
                <div className="row row-cols-4 g-4 mb-5 mt-5">
                  {sessionData.llm.map((llm) => (
                    <div className="col-3" key={llm.id}>
                      <LLMCard
                        id={id}
                        llm={llm}
                        fetchLLMData={fetchLLMData}
                        setSessionData={setSessionData}
                      />
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-5 text-center">
                  <p className="text-secondary">
                    Nessun LLM selezionato, aggiungi un LLM per cominciare.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
        <BlocksContextProvider>
          <div className="col-12">
            <div className="row row-cols-1">
              <div className="col">
                <TestForm sessionData={sessionData} />
              </div>
            </div>
          </div>
        </BlocksContextProvider>
      </div>
    </div>
  );
}
