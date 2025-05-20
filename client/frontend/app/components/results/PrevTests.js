"use client";

function formatTimestamp(ts) {
    const date = new Date(ts);
    return date.toLocaleString("it-IT", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
    });
}

export default function PrevTests({ prevTests, onTestClick }) {
    return (
        <>
            <h3 className="text-center text-primary">Test precedenti</h3>
            {prevTests.length === 0 ? (
                <p>Nessun test precedente trovato.</p>
            ) : (
                <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mt-2">
                    {prevTests.map((test) => (
                        <div className="col" key={test.id}>
                            <div className="card h-100 shadow-sm"
                                style={{ cursor: "pointer", userSelect: "none" }}
                                onClick={() => onTestClick && onTestClick(test)}
                                onMouseDown={e => e.preventDefault()}
                            >
                                <div className="card-body">
                                    <h5 className="card-title text-primary">
                                        Test #{test.id}
                                    </h5>
                                    <p className="mb-1">
                                        <strong>Blocco di domande:</strong>
                                        <br />
                                        <span className="text-dark">{test.block.name}</span>
                                    </p>
                                    <p className="mb-1">
                                        <strong>Data e ora:</strong>
                                        <br />
                                        <span className="text-dark">{formatTimestamp(test.timestamp)}</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </>
    );
}