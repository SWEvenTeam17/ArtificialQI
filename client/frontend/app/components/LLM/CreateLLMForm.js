import { getCSRFToken } from "@/app/helpers/csrf";
import Form from "next/form";
import { useState } from "react";

const CreateLLMForm = ({ fetchLLMList }) => {
    const [formErrors, setFormErrors] = useState({});
    const [name, setName] = useState("");
    const [parameters, setParameters] = useState("");

    const validateForm = () => {
        const errors = {};

        if (!name) {
            errors.name = "Il nome è obbligatorio.";
        }

        if (!parameters) {
            errors.n_parameters = "Il numero di parametri è obbligatorio.";
        }

        return errors;
    };

    const createLLM = async (e) => {
        e.preventDefault();
        const errors = validateForm();
        if(Object.keys(errors).length > 0) {
            setFormErrors(errors);
            return;
        }

        setFormErrors({});

        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            n_parameters: formData.get('nparameters'),
        };

        const JSONData = JSON.stringify(data);

        try {
            await fetch(`http://localhost:8000/llm_list/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json", "X-CSRFToken": getCSRFToken()
                },
                body: JSONData,
            });
            fetchLLMList();
            setName('');
            setParameters('');
        } catch (error) {
            console.error("Error submitting form:", error);
        }
    };

    return (
        <div className="mt-5">
            <Form className="mt-5" onSubmit={createLLM}>
                <p className="text-center fs-5">Crea un LLM:</p>
                <div className="form-floating mb-3">
                    <input
                        type="text"
                        id="name"
                        name="name"
                        className={`form-control mt-3 rounded-5 ${formErrors.name ? "is-invalid" : ""}`}
                        placeholder="Nome"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />
                    <label htmlFor="name">Nome</label>
                    {formErrors.name && <div className="invalid-feedback">{formErrors.name}</div>}
                </div>
                <div className="form-floating mb-3">
                    <input
                        type="text"
                        id="nparameters"
                        name="nparameters"
                        className={`form-control mt-3 rounded-5 ${formErrors.n_parameters ? "is-invalid" : ""}`}
                        placeholder="Numero Parametri"
                        value={parameters}
                        onChange={(e) => setParameters(e.target.value)}
                    />
                    <label htmlFor="description">Numero Parametri</label>
                    {formErrors.n_parameters && <div className="invalid-feedback">{formErrors.n_parameters}</div>}
                </div>
                <div className="text-center align-items-center col-12">
                    <button
                        type="submit"
                        className="btn btn-primary w-50 rounded-5"
                    >
                        Crea
                    </button>
                </div>
            </Form>
        </div>
    );
}

export default CreateLLMForm;