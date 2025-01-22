import Form from 'next/form';

const AddLLMForm = ({submitLLM, LLMData}) => {
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