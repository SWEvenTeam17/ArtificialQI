'use client'
import { useContext, useEffect, useState } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import SessionCard from './components/sessions/SessionCard';
import Form from 'next/form';

export default function Home() {
  const sessions = useContext(SessionContext);
  const [LLMList, setLLMList] = useState(null);
  const [selectedLLM, setSelectedLLM] = useState(null);

  useEffect(() => {
    fetchLLMList();
  }, []);

  const editLLM = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/llm_list/${selectedLLM.id}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({name: selectedLLM.name, n_parameters: selectedLLM.n_parameters}),
      });

      if (!response.ok) {
        throw new Error(`Failed to update LLM: ${response.statusText}`);
      }

      const data = await response.json();
      console.log(data);
      fetchLLMList();
    } catch (error) {
      console.error("Error updating LLM: ", error);
    }
  };

  const handleSelectLLM = (e) => {
    const selectedId = e.target.value;
    const object = LLMList.find((llm) => llm.id == selectedId);
    setSelectedLLM(object);
  }

  const fetchLLMList = async () => {
    fetch(`http://localhost:8000/llm_list`, {
      method: 'GET'
    })
    .then((response) => response.json())
    .then((data) => setLLMList(data))
    .catch((error) => {
      console.error("Error fetching LLM list:", error);
      setLLMList(null);
    });
  };

  return (
  <div className="container">
    <h1 className="text-center display-1 fw-medium mt-5 p-5">ArtificialQI</h1>
    <p className="text-center fs-5">Per cominciare, seleziona una sessione:</p>
    <div className="row row-cols-lg-4 row-cols-2 mt-5 g-2">
      {sessions.map((session, index) => (
        <SessionCard session={session} key={index} />
      ))}
    </div>

    <div className="mt-5">
      <p className="text-center fs-5">Modifica gli LLM esistenti:</p>
      <Form className="mt-5" onSubmit={editLLM}>
        <select
          className="form-select"
          name="selectllm"
          id="selectllm"
          value={selectedLLM ? selectedLLM.id : ""}
          onChange={handleSelectLLM}
          required
        >
          <option value="" disabled>
            Seleziona un LLM...
          </option>
          {LLMList ? LLMList.map((llm, index) => (
            <option key={index} value={llm.id}>{llm.name}</option>
          )) : <option disabled>Nessun LLM disponibile</option>}
        </select>
        <input
          type="text"
          className="form-control mt-3"
          placeholder="Nome"
          value={selectedLLM ? selectedLLM.name : ""}
          onChange={(e) => setSelectedLLM((prev) => ({ ...prev, name: e.target.value }))}
          disabled={!selectedLLM}
        />
        <input
          type="text"
          className="form-control mt-3"
          placeholder="Numero Parametri"
          value={selectedLLM ? selectedLLM.n_parameters : ""}
          onChange={(e) => setSelectedLLM((prev) => ({ ...prev, n_parameters: e.target.value }))}
          disabled={!selectedLLM}
        />
        <button type="submit" className="btn btn-primary mt-3" disabled={!selectedLLM}>
          Salva modifiche
        </button>
      </Form>
    </div>
  </div>);
}
