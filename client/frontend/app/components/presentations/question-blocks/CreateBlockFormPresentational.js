import React from "react";
import Form from 'next/form';

export default function CreateBlockFormPresentational({handleSubmit,questionAnswerPairs, formErrors, toastRef, inputRefs, handleInputChange, addQuestionAnswerPair, removeQuestionAnswerPair}) {
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
                    ref={(el) => (inputRefs.current["block_name"] = el)}
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
                        ref={(el) =>
                          (inputRefs.current[`question-${index}`] = el)
                        }
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
                        ref={(el) =>
                          (inputRefs.current[`answer-${index}`] = el)
                        }
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
