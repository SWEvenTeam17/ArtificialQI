"use client";
import { getCSRFToken } from "@/app/helpers/csrf";
import Form from "next/form";
import { useState, useRef } from "react";

export default function CreateQuestionBlock() {
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
    // Reset previous invalid styles
    Object.values(inputRefs.current).forEach(ref => {
      if (ref) {
        ref.classList.remove('is-invalid');
      }
    });

    e.preventDefault();

    let isValid = true;
    const currentErrors = {};

    const formData = new FormData(e.target);
    const blockName = formData.get("block_name");

    if (!blockName) {
      setFormErrors("Il nome del blocco è obbligatorio.");
      if (inputRefs.current['block_name']) {
        inputRefs.current['block_name'].classList.add('is-invalid');
      }
      isValid = false;
    }

    const updatedQuestionAnswerPairs = questionAnswerPairs.map((pair, index) => {
      const questionId = `question-${index}`;
      const answerId = `answer-${index}`;
      if (!pair.question) {
        currentErrors[questionId] = `La domanda numero ${index + 1} deve essere compilata.`;
        if (inputRefs.current[questionId]) {
          inputRefs.current[questionId].classList.add('is-invalid');
        }
        isValid = false;
      }
      if (!pair.answer) {
        currentErrors[answerId] = `La risposta numero ${index + 1} deve essere compilata.`;
        if (inputRefs.current[answerId]) {
          inputRefs.current[answerId].classList.add('is-invalid');
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
        }
      );

      if (response.status === 201) {
        e.target.reset();
        setQuestionAnswerPairs([{ question: "", answer: "" }]);
        // Reset invalid styles after successful submission
        Object.values(inputRefs.current).forEach(ref => {
          if (ref) {
            ref.classList.remove('is-invalid');
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
          if (inputRefs.current['block_name']) {
            inputRefs.current['block_name'].classList.add('is-invalid');
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

  return (
    <div className="container">
      <div className="card bg-light border-light rounded-5 m-5">
        <div className="card-body">
          <p className="card-title text-center fs-1 text-primary">
            Crea nuovo blocco
          </p>
          <Form
            onSubmit={handleSubmit}
            className="text-center justify-content-center"
          >
            {formErrors != "" ? (
              <div className="alert alert-danger" role="alert">
                {formErrors}
              </div>
            ) : null}

            <div className="row text-center justify-content-center m-3 ">
              <div className="col-12 col-md-6">
                <div className="form-floating">
                  <input
                    ref={(el) => (inputRefs.current['block_name'] = el)}
                    id="block_name"
                    name="block_name"
                    className="form-control rounded-5"
                    placeholder="Nome blocco"
                  />
                  <label htmlFor="block_name">Nome del blocco</label>
                </div>
              </div>
            </div>
            {questionAnswerPairs.map((pair, index) => (
              <div key={index}>
                <div className="row g-3 align-items-center">
                  <div
                    className={`${questionAnswerPairs.length > 1 ? "col-md-5" : "col-md-6"} col-12`}
                  >
                    <div className="form-floating">
                      <input
                        ref={(el) => (inputRefs.current[`question-${index}`] = el)}
                        type="text"
                        className="form-control rounded-5"
                        id={`question-${index}`}
                        name="question"
                        placeholder={`Domanda numero ${index + 1}`}
                        value={pair.question}
                        onChange={(e) => handleInputChange(index, e)}
                      />
                      <label htmlFor={`question-${index}`}>
                        {`Domanda numero ${index + 1}`}
                      </label>
                    </div>
                  </div>
                  <div
                    className={`${questionAnswerPairs.length > 1 ? "col-md-5" : "col-md-6"} col-12`}
                  >
                    <div className="form-floating">
                      <input
                        ref={(el) => (inputRefs.current[`answer-${index}`] = el)}
                        type="text"
                        className="form-control rounded-5"
                        id={`answer-${index}`}
                        name="answer"
                        placeholder={`Risposta attesa numero ${index + 1}`}
                        value={pair.answer}
                        onChange={(e) => handleInputChange(index, e)}
                      />
                      <label htmlFor={`answer-${index}`}>
                        {`Risposta attesa numero ${index + 1}`}
                      </label>
                    </div>
                  </div>
                  {questionAnswerPairs.length > 1 && (
                    <div className="col-12 col-md-2">
                      <button
                        className="btn btn-danger rounded-5 w-100"
                        onClick={(e) => {
                          e.preventDefault();
                          removeQuestionAnswerPair(index);
                        }}
                      >
                        X
                      </button>
                    </div>
                  )}
                </div>
                <hr />
              </div>
            ))}

            <div className="row row-cols-md-2 row-cols-1 g-3">
              <div className="col">
                <button
                  type="submit"
                  className="btn btn-primary rounded-5 w-100"
                >
                  Crea blocco
                </button>
              </div>
              <div className="col">
                <button
                  className="btn btn-outline-info w-100 rounded-5"
                  onClick={(e) => {
                    e.preventDefault();
                    addQuestionAnswerPair();
                  }}
                >
                  Aggiungi una domanda
                </button>
              </div>
            </div>
          </Form>
          <div
            className="position-fixed bottom-0 end-0 p-3"
            style={{ zIndex: 11 }}
          >
            <div
              ref={toastRef}
              className="toast align-items-center text-bg-success border-0"
              role="alert"
              aria-live="assertive"
              aria-atomic="true"
            >
              <div className="d-flex">
                <div className="toast-body">Blocco creato con successo!</div>
                <button
                  type="button"
                  className="btn-close btn-close-white me-2 m-auto"
                  data-bs-dismiss="toast"
                  aria-label="Close"
                ></button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}