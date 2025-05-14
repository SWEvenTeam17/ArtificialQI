import { createContext, useContext, useState } from "react";

const BlocksContext = createContext();

export const useBlocksContext = () => {
  return useContext(BlocksContext);
};

export const BlocksContextProvider = ({ children }) => {
  const [selectedBlocks, setSelectedBlocks] = useState([]);

  const addBlock = async (id) => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`,
      {
        method: "GET",
      },
    );
    let data = await response.json();
    setSelectedBlocks((prevBlocks) => [...prevBlocks, data]);
  };

  const removeBlock = async (id) => {
    setSelectedBlocks((prevBlocks) => {
      return prevBlocks.filter((block) => block.id !== id);
    });
  };

  return (
    <BlocksContext.Provider
      value={{
        selectedBlocks,
        setSelectedBlocks,
        addBlock,
        removeBlock,
      }}
    >
      {children}
    </BlocksContext.Provider>
  );
};
