"use client";

import { TestComparatorContextProvider } from "../components/contexts/test-comparator/TestComparatorContext";

export default function Layout({ children }) {
  return (
    <TestComparatorContextProvider>{children}</TestComparatorContextProvider>
  );
}
