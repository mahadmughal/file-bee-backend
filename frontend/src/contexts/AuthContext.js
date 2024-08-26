import { useContext, createContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = JSON.parse(localStorage.getItem("authToken"));

    if (storedToken) {
      setToken(storedToken);

      if (!user) {
        getUserDetails(storedToken);
      }
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
          const tokenToStore = {
            key: data.token.key,
            expiresAt: data.token.expires_at,
          };

          setToken(tokenToStore);
          setUser(data.token.user);

          try {
            localStorage.setItem("authToken", JSON.stringify(tokenToStore));
            // After setting the token, navigate to root
            navigate("/");
          } catch (error) {
            console.error("Failed to store auth token:", error);
            // Handle the error (e.g., show a notification to the user)
          }
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const getUserDetails = async (token) => {
    try {
      const response = await fetch("http://localhost:8000/api/user/", {
        method: "GET",
        headers: {
          Authorization: `Token ${token.key}`,
        },
      });

      if (response.status === 401) {
        navigate("/sign_in");
      } else if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || "Login failed");
      } else {
        const data = await response.json();
        console.log("User login successful:", data);
        if (data.token && data.token.user) {
          setUser(data.token.user);
        }
      }
    } catch (err) {
      console.error(err);
    }
  };

  const logOut = () => {
    setUser(null);
    setToken(null);
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
