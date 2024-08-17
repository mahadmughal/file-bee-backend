import { useContext, createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("authToken");
    if (storedToken) {
      setToken(storedToken);
      // Optionally fetch user data here if needed
    }
    setLoading(false);
  }, []);

  const loginAction = async (data) => {
    try {
      const response = await fetch("http://localhost:8000/api/user/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || "Login failed");
        return;
      } else {
        const data = await response.json();
        console.log("User login successful:", data);

        if (data.token && data.token.key) {
          setUser(data.user);
          setToken(data.token);
          localStorage.setItem("authToken", data.token.key);

          // After setting the token, navigate to root
          navigate("/");

          return;
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const logOut = () => {
    setUser(null);
    setToken("");
    localStorage.removeItem("authToken");
    navigate("/sign_in");
  };

  if (loading) {
    return <div>Loading...</div>; // Or any loading indicator
  }

  return (
    <AuthContext.Provider value={{ token, user, loginAction, logOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};
