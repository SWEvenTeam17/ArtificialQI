import { useState, useRef } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
import { useQuestionBlockContext } from "@/app/components/contexts/question-blocks/QuestionBlockContext";

export const useCreateBlockFormHook = () => {
  const { addQuestionBlock } = useQuestionBlockContext();

  const [questionAnswerPairs, setQuestionAnswerPairs] = useState([
    { question: "", answer: "" },
  ]);

  const [formErrors, setFormErrors] = useState("");
  const toastRef = useRef(null);
  const inputRefs = useRef({});

  const handleInputChange = (index, e) => {
    const { name, value } = e.target;
    const newArray = [...questionAnswerPairs];
    newArray[index][name] = value;
    setQuestionAnswerPairs(newArray);
  };

  const addQuestionAnswerPair = () => {
    setQuestionAnswerPairs([
      ...questionAnswerPairs,
      { question: "", answer: "" },
    ]);
  };

  const removeQuestionAnswerPair = (index) => {
    setQuestionAnswerPairs(questionAnswerPairs.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    setFormErrors("");
    Object.values(inputRefs.current).forEach((ref) => {
      if (ref) {
        ref.classList.remove("is-invalid");
      }
    });

    e.preventDefault();

    let isValid = true;
    const currentErrors = {};

    const formData = new FormData(e.target);
    const blockName = formData.get("block_name");

    if (!blockName) {
      setFormErrors("Il nome del blocco è obbligatorio.");
      if (inputRefs.current["block_name"]) {
        inputRefs.current["block_name"].classList.add("is-invalid");
      }
      isValid = false;
    }

    questionAnswerPairs.map((pair, index) => {
      const questionId = `question-${index}`;
      const answerId = `answer-${index}`;
      if (!pair.question) {
        currentErrors[questionId] =
          `La domanda numero ${index + 1} deve essere compilata.`;
        if (inputRefs.current[questionId]) {
          inputRefs.current[questionId].classList.add("is-invalid");
        }
        isValid = false;
      }
      if (!pair.answer) {
        currentErrors[answerId] =
          `La risposta numero ${index + 1} deve essere compilata.`;
        if (inputRefs.current[answerId]) {
          inputRefs.current[answerId].classList.add("is-invalid");
        }
        isValid = false;
      }
      return pair;
    });

    if (!isValid) {
      if (!formErrors && Object.keys(currentErrors).length > 0) {
        setFormErrors("Assicurati di compilare tutti i campi obbligatori.");
      }
      return;
    }

    const formatted = questionAnswerPairs.map((pair) => ({
      question: pair.question,
      answer: pair.answer,
    }));

    const data = {
      name: blockName,
      questions: formatted,
    };

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify(data),
        },
      );

      if (response.status === 201) {
        const newBlock = await response.json();
        addQuestionBlock(newBlock);
        e.target.reset();
        setQuestionAnswerPairs([{ question: "", answer: "" }]);
        Object.values(inputRefs.current).forEach((ref) => {
          if (ref) {
            ref.classList.remove("is-invalid");
          }
        });
        setFormErrors("");
        if (toastRef.current) {
          const toast = new bootstrap.Toast(toastRef.current);
          toast.show();
        }
      } else {
        const errorData = await response.json().catch(() => null);
        if (errorData?.error === "Nome duplicato") {
          setFormErrors("Esiste già un blocco con questo nome.");
          if (inputRefs.current["block_name"]) {
            inputRefs.current["block_name"].classList.add("is-invalid");
          }
        } else {
          setFormErrors("Errore durante la creazione del blocco.");
        }
      }
    } catch (error) {
      console.error("Errore durante la creazione del blocco:", error);
      setFormErrors("Errore di rete durante la creazione del blocco.");
    }
  };

  return {
    questionAnswerPairs,
    formErrors,
    toastRef,
    inputRefs,
    handleSubmit,
    handleInputChange,
    addQuestionAnswerPair,
    removeQuestionAnswerPair,
  };
};
