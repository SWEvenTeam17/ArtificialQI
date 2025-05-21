import { createContext, useContext, useEffect } from "react";
import { useState } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";

const SessionContext = createContext();

export const useSessionContext = () => {
  return useContext(SessionContext);
};

export const SessionContextProvider = ({ children }) => {
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/`,
      );
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  const deleteSession = async (id) => {
    let data = {
      id: id,
    };
    const JSONData = JSON.stringify(data);
    try {
      await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}/`,
        {
          method: "DELETE",
          headers: {
            "Content-type": "application/josn",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSONData,
        },
      );
      fetchSessions();
    } catch (error) {
      console.error("Error deleting form: ", error);
    }
  };

  const updateSession = async (id, updatedData) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/session_list/${id}/`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
          body: JSON.stringify(updatedData),
        },
      );
      if (response.ok) {
        fetchSessions();
      }
    } catch (error) {
      console.error("Error updating session: ", error);
    }
  };

  return (
    <SessionContext.Provider
      value={{ sessions, fetchSessions, deleteSession, updateSession }}
    >
      {children}
    </SessionContext.Provider>
  );
};
