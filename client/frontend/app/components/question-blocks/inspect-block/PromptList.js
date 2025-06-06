import PromptCard from "./PromptCard";

export default function PromptList({ prompts }) {
  return (
    <div className="row row-cols-1 row-cols-md-2 g-4">
      {prompts.map((prompt) => (
        <div className="col" key={prompt.id}>
          <PromptCard prompt={prompt} />
        </div>
      ))}
    </div>
  );
}
