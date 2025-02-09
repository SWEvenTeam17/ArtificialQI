import { useState, useEffect } from 'react';

const PreviousTestsCard = ({id})=>{

    const [previousTests, setPreviousTests] = useState([]);

    useEffect(()=>{
        fetchPreviousTests();
    },[]);

    const fetchPreviousTests = async ()=>{
        let response = await fetch(`http://localhost:8000/previous_tests/${id}/`);
        let data = await response.json();
        console.log(data);
        setPreviousTests(data);
    };

    const deletePreviousTest = async (id) => {
        let response = await fetch(`http://localhost:8000/previous_tests/${id}/`, {
            method: "DELETE",
            body:{"previousPromptId":id}
        });
        if (response.status === 204) {
            setPreviousTests((prevTests) => {
                return prevTests.filter((test) => {test.id !== testId});
            });
        }

    };

    return(<div></div>);
}

export default PreviousTestsCard;