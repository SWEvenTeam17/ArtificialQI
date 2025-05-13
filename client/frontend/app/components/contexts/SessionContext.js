import { createContext } from "react";

export const SessionContext = createContext({
  sessions: [],
  deleteSession: () => {},
  updateSession: () => {},
});
