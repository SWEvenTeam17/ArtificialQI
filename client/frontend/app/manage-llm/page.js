"use client";
import { useEffect, useState } from "react";
import GeneralLLMCard from "../components/LLM/GeneralLLMCard";
import CreateLLMForm from "../components/LLM/CreateLLMForm";

export default function ManageLLM() {
  const [LLMList, setLLMList] = useState([]);

  useEffect(() => {
    fetchLLMList();
  }, []);

  const fetchLLMList = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/llm_list/`
      );
      const data = await response.json();
      setLLMList(data);
    } catch (error) {
      console.error("Error fetching LLM list:", error);
    }
  };

  return (
    <div className="container">
      <div className="card shadow border-light rounded-5 mt-3">
        <div className="card-body">
          <h2 className="card-title text-center">Gestisci LLM</h2>
          <div className="row mb-5 justify-content-center">
            <div className="col-12 col-md-6">
              <CreateLLMForm fetchLLMList={fetchLLMList} />
            </div>
          </div>
          <h2 className="card-title text-center mb-4">
            LLM collegati ad ArtificialQI
          </h2>
          {LLMList.length > 0 ? (
            <div className="row g-2 row-cols-1 row-cols-md-2">
              {LLMList.map((llm) => (
                <div className="col" key={llm.id}>
                  <GeneralLLMCard llm={llm} fetchLLMList={fetchLLMList} />
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center">Nessun LLM disponibile</p>
          )}
        </div>
      </div>
    </div>
  );
}
