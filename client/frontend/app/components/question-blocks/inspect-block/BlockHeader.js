export default function BlockHeader({ name, promptCount }) {
  return (
    <div className="text-center mb-4">
      <h1 className="text-primary">Insieme: {name}</h1>
      <h4 className="text-muted">Contiene {promptCount} prompt</h4>
    </div>
  );
}
