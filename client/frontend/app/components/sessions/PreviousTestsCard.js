import { useState, useEffect } from 'react';
import { useQuestionsContext } from '../contexts/QuestionsContext';
import { getCSRFToken } from '@/app/helpers/csrf';

const PreviousTestsCard = ({ id }) => {
    const [previousTests, setPreviousTests] = useState([]);
    const { selectedQuestions, setSelectedQuestions, addQuestion, removeQuestion } = useQuestionsContext();

    useEffect(() => {
        fetchPreviousTests();
    }, []);

    const fetchPreviousTests = async () => {
        let response = await fetch(`http://localhost:8000/previous_tests/${id}/`);
        let data = await response.json();
        setPreviousTests(data);
    };

    const deletePreviousTest = async (testId) => {
        let response = await fetch(`http://localhost:8000/previous_tests/${testId}/`, {
            method: "DELETE",
            body: JSON.stringify({ "previousPromptId": testId }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken()
            },
        });
        if (response.status === 204) {
            setPreviousTests((prevTests) => {
                return prevTests.filter((test) => test.id !== testId);
            });
        }
    };

    const isSelected = (questionId) => {
        return selectedQuestions.some((q) => q.id === questionId);
    };

    return (
        previousTests.length > 0 ? (
            <div className="row row justify-content-center" style={{ minHeight: '220px' }}>
                <div className="col-12 col-md-8">
                    <div className='card border-light shadow-lg rounded-4 mb-5'>
                        <div className='card-body'>
                            <h5 className="card-title text-center text-primary font-weight-bold">Test precedenti</h5>
                            <ul className='list-group list-group-flush'>
                                {previousTests.map((pTest) => (
                                    <a href="#" key={pTest.id} className="list-group-item list-group-item-action rounded-3">
                                        <div className="d-flex w-100 justify-content-between">
                                            <h5 className="mb-1">{pTest.prompt_text}</h5>
                                        </div>
                                        <p className="mb-1">{pTest.expected_answer}</p>
                                        <div className='row row-cols-1 row-cols-md-2'>
                                            <div className='col'>
                                                {isSelected(pTest.id) ? (
                                                    <button
                                                        className='btn btn-outline-success rounded-5 w-100'
                                                        onClick={(e) => {
                                                            e.preventDefault();
                                                            removeQuestion(pTest.id);
                                                        }}
                                                    >
                                                        Rimuovi
                                                    </button>
                                                ) : (
                                                    <button
                                                        className='btn btn-success rounded-5 w-100'
                                                        onClick={(e) => {
                                                            e.preventDefault();
                                                            addQuestion(pTest.id);
                                                        }}
                                                    >
                                                        Seleziona
                                                    </button>
                                                )}
                                            </div>
                                            <div className='col'>
                                                <button
                                                    className='btn btn-danger rounded-5 w-100'
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        deletePreviousTest(pTest.id);
                                                    }}
                                                >
                                                    Elimina
                                                </button>
                                            </div>
                                        </div>
                                    </a>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        ) : (null)
    );
};

export default PreviousTestsCard;
