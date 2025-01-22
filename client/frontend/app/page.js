'use client'
import { useContext, useEffect, useState } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import SessionCard from './components/sessions/SessionCard';
import EditLLMForm from './components/LLM/EditLLMForm';
export default function Home() {
  const sessions = useContext(SessionContext);
  const [LLMList, setLLMList] = useState(null);

  useEffect(() => {
    fetchLLMList();
  }, []);

  const fetchLLMList = async () => {
    fetch(`http://localhost:8000/llm_list`, {
      method: 'GET',
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

    </div>
  );
}
