'use client'
import { useResponse } from "@/app/components/contexts/ResponseContext";

export default function ResultsPage() {
    const { responseData } = useResponse();

    return (
        <div className="container">
            <h1 className="text-center mb-5">Results</h1>
            <div className="row row-cols-1 row-cols-md-3 row-cols-lg-4 g-4 mb-5 p-5">
                {responseData && responseData.length > 0 ? (
                    responseData.map((response, index) => (
                        <div className="col" key={index}>
                            <div className="card shadow-sm border-light rounded-lg">
                                <div className="card-body">
                                    <h5 className="card-title text-primary">{response.llm_name}</h5>
                                    <p className="card-text text-muted">{response.answer}</p>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <p>No results available</p>
                )}
            </div>
        </div>
    );
}
