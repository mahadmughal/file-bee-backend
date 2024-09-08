import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import AlertComponent from "../components/Alert";

const AlertContext = createContext();

export const AlertProvider = ({ children }) => {
  const [alert, setAlert] = useState(null);

  const addAlert = useCallback((newAlert) => {
    setAlert(newAlert);
  }, []);

  const removeAlert = useCallback(() => {
    setAlert(null);
  }, []);

  // Auto-remove alert after 5 seconds
  useEffect(() => {
    if (alert) {
      const timer = setTimeout(() => {
        removeAlert();
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [alert, removeAlert]);

  return (
    <AlertContext.Provider value={{ addAlert, removeAlert }}>
      {children}
      <div className="fixed-top" style={{ zIndex: 1050 }}>
        {alert && <AlertComponent {...alert} onClose={removeAlert} />}
      </div>
    </AlertContext.Provider>
  );
};

export const useAlert = () => {
  const context = useContext(AlertContext);
  if (!context) {
    throw new Error("useAlert must be used within an AlertProvider");
  }
  return context;
};
