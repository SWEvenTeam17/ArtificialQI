import React from 'react'
import { useState, useEffect } from 'react';
import InspectBlockPagePresentational from '../../presentations/question-blocks/InspectBlockPagePresentational';

export default function InspectBlockPageContainer({id}) {
  const [blockData, setBlockData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBlockData = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}`,
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

  useEffect(() => {
    fetchBlockData();
  }, []);
  return (
    <InspectBlockPagePresentational blockData={blockData} setBlockdata={setBlockData} loading={loading} error={error}/>
  )
}
