import React from "react";
import PromptCardPresentational from "../../presentations/question-blocks/PromptCardPresentational";

export default function PromptCardContainer({ prompt, blockData, setBlockData }) {
  const deletePrompt = async (promptId) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_list/${promptId}/`,
        {
          method: "DELETE",
        }
      );

      if (response.status === 204) {
        const updatedPrompts = blockData.prompt.filter(
          (prompt) => prompt.id !== promptId
        );
        setBlockData({ ...blockData, prompt: updatedPrompts });
      } else {
        console.error("Errore nella cancellazione del prompt");
      }
    } catch (err) {
      console.error("Errore nella richiesta:", err);
    }
  };
  return <PromptCardPresentational prompt={prompt} deletePrompt={deletePrompt}/>;
}
