
import { useInspectBlockContext } from "@/app/components/contexts/InspectBlockContext";
import BlockHeader from "./BlockHeader";
import PromptList from "./PromptList";
import PromptResults from "./PromptResults";

export default function InspectBlockPage() {
  const {
    blockData,
    testResults,
    uniqueId,
    loading,
    error,
    deletePrompt,
    handleView,
    handleEdit
  } = useInspectBlockContext();

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border text-primary" role="status" />
        <p className="mt-3">Caricamento in corso...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger text-center mt-4" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="container py-4">
      <BlockHeader name={blockData.name} promptCount={blockData.prompt?.length || 0} />

      <PromptList
        prompts={blockData.prompt}
        onDelete={deletePrompt}
        onView={handleView}
        onEdit={handleEdit}
      />

      {testResults && (
        <PromptResults key={uniqueId} />
      )}
    </div>
  );
}
