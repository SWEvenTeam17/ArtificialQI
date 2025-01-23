import Form from 'next/form';

const AddLLMForm = ({LLMData, sessionData, setSessionData, fetchLLMData}) => {

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

    return (
    <Form onSubmit={submitLLM}>
        <select
            className="form-select"
            name="selectllm"
            id="selectllm"
            defaultValue=""
            required
        >
            <option value="" disabled>
                Seleziona un LLM...
            </option>
            {LLMData ? LLMData.map((llm, index) => (
                <option key={index} value={llm.id}>{llm.name}</option>
            )) : "ciao"}
        </select>
        <button className="btn btn-primary" type="submit">
            Aggiungi
        </button>
    </Form>);
}

export default AddLLMForm;