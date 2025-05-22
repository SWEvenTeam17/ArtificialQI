"use client";
import React from "react";
import { LLMManagerContextProvider } from "../components/contexts/LLMManagerContext";
export default function Layout({ children }) {
  return (
      <LLMManagerContextProvider>
        {children}
      </LLMManagerContextProvider>
  );
}
