import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext({
  currentUser: null,
  setCurrentUser: () => {},
  token: null,
  setToken: () => {},
});

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("authToken");
    if (storedToken) {
      setToken(storedToken);
      // You can potentially fetch user data based on token here
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{ currentUser, setCurrentUser, token, setToken }}
    >
      {children}
    </AuthContext.Provider>
  );
};
