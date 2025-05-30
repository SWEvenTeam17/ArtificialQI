"use client";

import { LLMManagerContextProvider } from "../components/contexts/llm-manager/LLMManagerContext";
export default function Layout({ children }) {
  return (
      <LLMManagerContextProvider>
        {children}
      </LLMManagerContextProvider>
  );
}
