
export default async function Home() {
  const response = await fetch("http://127.0.0.1:8000/session_list");
  const sessions = await response.json();
  return (
    <div className="container">
      {sessions.map((session) => (
        <p id={session.id}>{session.name}</p> 
      ))}
    </div>
  );
}
