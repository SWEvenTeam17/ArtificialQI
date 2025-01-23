import Form from "next/form";

const CreateLLMForm = ({fetchLLMList}) => {

    const createLLM = async (e) => {
        e.preventDefault();

        const formData = new FormData(e.target);
        const data = {
            name: formData.get('name'),
            n_parameters: formData.get('nparameters'),
        };

        const JSONData = JSON.stringify(data);

        try {
            const response = await fetch(`http://localhost:8000/llm_list/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSONData,
            });

            fetchLLMList();
            e.target.reset();
        } catch (error) {
            console.error("Error submitting form:", error);
        }
    };

    return (
        <div className="mt-5">
            <p className="text-center fs-5">Crea un LLM:</p>
            <Form className="mt-5" onSubmit={createLLM}>
                <div className="form-floating mb-3">
                    <input
                        type="text"
                        id="name"
                        name="name"
                        className="form-control mt-3"
                        placeholder="Nome"
                    />
                    <label htmlFor="name">Nome</label>
                </div>
                <div className="form-floating mb-3">
                    <input
                        type="text"
                        id="nparameters"
                        name="nparameters"
                        className="form-control mt-3"
                        placeholder="Numero Parametri"
                    />
                    <label htmlFor="description">Numero Parametri</label>
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