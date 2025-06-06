"use client";

import { useState, useEffect, createContext, useContext } from "react";

const TestComparatorContext = createContext();

export const useTestComparatorContext = () => {
  return useContext(TestComparatorContext);
};

export const TestComparatorContextProvider = ({ children }) => {
  const [selectedSessionData, setSelectedSessionData] = useState([]);
  const [selectedLLMS, setSelectedLLMS] = useState({
    firstLLM: "",
    secondLLM: "",
  });
  const [llmNames, setLlmNames] = useState({});
  const [blockComparisonData, setBlockComparisonData] = useState([]);

  const fetchSessionData = async (id) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}`,
    );
    const data = await response.json();
    setSelectedSessionData(data);

    const namesMap = {};
    data.llm.forEach((llm) => {
      namesMap[llm.id] = llm.name;
    });
    setLlmNames(namesMap);
  };

  const fetchBlockComparisonData = async (firstLLM, secondLLM) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/compare/?first_llm_id=${firstLLM}&second_llm_id=${secondLLM}`,
    );
    const data = await response.json();
    setBlockComparisonData(data.common_blocks);
    console.log(data);
  };

  useEffect(() => {
    if (selectedLLMS.firstLLM && selectedLLMS.secondLLM) {
      fetchBlockComparisonData(selectedLLMS.firstLLM, selectedLLMS.secondLLM);
    }
  }, [selectedLLMS]);

  const chartData = blockComparisonData.map((block) => ({
    block: block.block_name,
    [`${llmNames[selectedLLMS.firstLLM]} - Semantica`]:
      block.llms[selectedLLMS.firstLLM]?.semantic_avg,
    [`${llmNames[selectedLLMS.secondLLM]} - Semantica`]:
      block.llms[selectedLLMS.secondLLM]?.semantic_avg,
    [`${llmNames[selectedLLMS.firstLLM]} - Esterna`]:
      block.llms[selectedLLMS.firstLLM]?.external_avg,
    [`${llmNames[selectedLLMS.secondLLM]} - Esterna`]:
      block.llms[selectedLLMS.secondLLM]?.external_avg,
  }));
  return (
    <TestComparatorContext.Provider
      value={{
        selectedSessionData,
        setSelectedSessionData,
        selectedLLMS,
        setSelectedLLMS,
        llmNames,
        setLlmNames,
        blockComparisonData,
        setBlockComparisonData,
        fetchSessionData,
        fetchBlockComparisonData,
        chartData,
      }}
    >
      {children}
    </TestComparatorContext.Provider>
  );
};
