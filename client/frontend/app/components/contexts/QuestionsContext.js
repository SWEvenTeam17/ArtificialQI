import { createContext, useContext, useState, useEffect } from "react";

const QuestionsContext = createContext();

export const useQuestionsContext = () => {
  return useContext(QuestionsContext);
};

export const QuestionsContextProvider = ({ children }) => {
  const [selectedQuestions, setSelectedQuestions] = useState([]);

  const addQuestion = async (id) => {
    let response = await fetch(`http://backend:8000/prompt_list/${id}/`, {
      method: "GET",
    });
    let data = await response.json();
    setSelectedQuestions((prevQuestions) => [...prevQuestions, data]);
  };

  const removeQuestion = async (id) => {
    setSelectedQuestions((prevQuestions) => {
      return prevQuestions.filter((question) => question.id !== id);
    });
  };

  useEffect(() => {
    console.log(selectedQuestions);
  }, [selectedQuestions]);

  return (
    <QuestionsContext.Provider
      value={{
        selectedQuestions,
        setSelectedQuestions,
        addQuestion,
        removeQuestion,
      }}
    >
      {children}
    </QuestionsContext.Provider>
  );
};
