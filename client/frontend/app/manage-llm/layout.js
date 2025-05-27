"use client";

import { LLMManagerContextProvider } from "../components/contexts/LLMManagerContext";
export default function Layout({ children }) {
  return (
      <LLMManagerContextProvider>
        {children}
      </LLMManagerContextProvider>
  );
}
