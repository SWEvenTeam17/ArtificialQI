
export default async function Home() {
  const response = await fetch("http://127.0.0.1:8000/session_list");
  const sessions = await response.json();
  return (
    <div className="container">
      <div className="text-center mt-5">
        <h1 className="fw-light fs-1 fw-bold">ArtificialQi</h1>
        <p className="fw-light">Seleziona una sessione per cominciare.</p>
      </div>
      <div key="menu" className="row row-cols-2 row-cols-md-4 g-2 mt-5">
        {sessions.map((session) => (
          <div className="col">
            <a className="card text-bg-light hover-grow text-decoration-none rounded-5 shadow h-100 w-100 text-center" key={session.id} id={session.id}>
              <div className="card-body">
                <div className="card-title">{session.title}</div>
                <div className="card-text">{session.description}</div>
              </div>
            </a>
          </div>
        ))
        }
        <div className="col d-flex justify-content-center align-items-center">
          <a className="card border-primary text-bg-light hover-grow text-decoration-none align-items-center rounded-5 shadow w-100 text-center">
            <div className="card-body">
              <div className="card-title">Aggiungi sessione</div>
            </div>
          </a>
        </div>
      </div>
    </div>
  );
}
