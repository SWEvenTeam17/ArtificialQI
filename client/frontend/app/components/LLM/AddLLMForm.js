import Form from 'next/form';

const AddLLMForm = ({ LLMData, sessionData, setSessionData, fetchLLMData }) => {

    const submitLLM = async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const data = {
            sessionId: sessionData.id,
            llmId: formData.get('selectllm')
        }
        const JSONData = JSON.stringify(data);

        const response = await fetch("http://localhost:8000/llm_add/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSONData
        });
        const result = await response.json();
        setSessionData((prevSessionData) => ({
            ...prevSessionData,
            llm: [...prevSessionData.llm, result]
        }));
        fetchLLMData();
    };

    const isLLMDataEmpty = !LLMData || LLMData.length === 0;

    return (
        <div className='card rounded-4'>
            <div className='card-body'>
                <h3 className="card-title">Large Language Models connessi</h3>

                <Form onSubmit={submitLLM}>
                    {isLLMDataEmpty ? (
                        <p className="text-center text-muted">Nessun LLM disponibile</p>
                    ) : (
                        <select
                            className="form-select mt-4 mb-4 text-center"
                            name="selectllm"
                            id="selectllm"
                            defaultValue=""
                            required
                            disabled={isLLMDataEmpty}
                        >
                            <option value="" disabled>
                                Seleziona un LLM...
                            </option>
                            {LLMData.map((llm, index) => (
                                <option key={index} value={llm.id}>{llm.name}</option>
                            ))}
                        </select>
                    )}
                    <button className="btn btn-primary w-100" type="submit" disabled={isLLMDataEmpty}>
                        Aggiungi
                    </button>
                </Form>
            </div>
        </div>
    );
}

export default AddLLMForm;
