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
    const user = JSON.parse(localStorage.getItem("user"));

    if (storedToken) {
      const expirationDate = new Date(storedToken.expiresAt);
      const currentDate = new Date();

      if (currentDate > expirationDate) {
        // Token has expired
        console.log("Token has expired. Redirecting to sign-in page.");
        localStorage.removeItem("authToken");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
        navigate("/sign_in");
      } else {
        // Token is still valid
        setToken(storedToken);
        if (user) {
          setUser(user);
        } else {
          getUserDetails(storedToken);
        }
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
            localStorage.setItem("user", JSON.stringify(data.token.user));
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

  const updateUser = (updatedUserData) => {
    setUser(updatedUserData);
    localStorage.setItem("user", JSON.stringify(updatedUserData));
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
    <AuthContext.Provider
      value={{ token, user, loginAction, logOut, updateUser }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;

export const useAuth = () => {
  return useContext(AuthContext);
};
