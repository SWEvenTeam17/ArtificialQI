
export default async function Home() {
  const response = await fetch("http://127.0.0.1:8000/session_list");
  const sessions = await response.json();
  return (
    <div className="container">
      <div className="text-center mt-5">
      <h1 className="fw-light fs-1 fw-bold">ArtificialQi</h1>
      <p className="fw-light">Seleziona una sessione per cominciare.</p>
      </div>
      <div className="row row-cols-2 row-cols-md-4 g-2 mt-5">
        {sessions.length > 0 ? (
          sessions.map((session) => (
            <div className="col">
              <div className="card h-100 w-100 text-center" key={session.id} id={session.id}>
                <div className="card-body">
                  <div className="card-title">{session.title}</div>
                  <div className="card-text">{session.description}</div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p>No sessions available.</p>
        )}
      </div>
    </div>
  );
}
