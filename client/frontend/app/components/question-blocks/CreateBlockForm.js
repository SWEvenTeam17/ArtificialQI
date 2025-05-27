
import Form from "next/form";
import { useCreateBlockFormHook } from "../hooks/QuestionBlocks/CreateBlockFormHook";
import { BlockNameInput } from "./BlockNameInput";
import { QuestionAnswerRow } from "./QuestionAnswerRow";
import { SuccessToast } from "./SuccessToast";

export default function CreateBlockForm() {
  const {
    inputRefs,
    toastRef,
    handleSubmit,
    handleInputChange,
    addQuestionAnswerPair,
    removeQuestionAnswerPair,
    formErrors,
    questionAnswerPairs,
  } = useCreateBlockFormHook();

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
            {formErrors && (
              <div className="alert alert-danger" role="alert">
                {formErrors}
              </div>
            )}

            <BlockNameInput inputRefs={inputRefs} />

            {questionAnswerPairs.map((pair, index) => (
              <QuestionAnswerRow
                key={index}
                pair={pair}
                index={index}
                inputRefs={inputRefs}
                onChange={handleInputChange}
                onRemove={removeQuestionAnswerPair}
                canRemove={questionAnswerPairs.length > 1}
              />
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

          <SuccessToast toastRef={toastRef} />
        </div>
      </div>
    </div>
  );
}
