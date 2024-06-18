import React from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import bgImage from "../../assets/images/photo22@2x.jpg";

function SignIn() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null); // State for error handling

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username) {
      setError("Username must not be empty");
      return;
    }

    if (!password) {
      setError("Password must not be empty");
      return;
    }

    const url = "http://localhost:8000/api/user/login/";
    const header = { "X-CSRFTOKEN": getCookie("csrftoken") };
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
      const response = await fetch(url, {
        method: "POST",
        header,
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || "Login failed");
      } else {
        console.log("User login successful:", response);
        navigate("/");
      }
    } catch (error) {
      setError(error);
      console.error("Fetch error: ", error);
    }
  };

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const handleErrorClose = (e) => {
    setError(null);
  };

  return (
    <div id="page-container">
      <main id="main-container">
        <div
          className="bg-image"
          style={{ backgroundImage: `url(${bgImage})` }}
        >
          <div className="row no-gutters bg-primary-op">
            <div className="hero-static col-md-6 d-flex align-items-center bg-white">
              <div className="p-3 w-100">
                <div className="mb-3 text-center">
                  <Link to="/" className="link-fx font-w700 font-size-h1">
                    <span className="text-dark">File</span>
                    <span className="text-primary">Bee</span>
                  </Link>
                  <p className="text-uppercase font-w700 font-size-sm text-muted">
                    Sign In
                  </p>
                </div>
                <div className="row no-gutters justify-content-center">
                  <div className="col-sm-8 col-xl-6">
                    <form
                      className="js-validation-signin"
                      action="be_pages_auth_all.html"
                      method="POST"
                    >
                      {error && (
                        <div
                          class="alert alert-danger d-flex align-items-center justify-content-between"
                          role="alert"
                        >
                          <div class="flex-fill mr-3">
                            <p class="mb-0">{error}</p>
                          </div>
                          <div class="flex-00-auto">
                            <i
                              class="fa fa-fw fa-times-circle"
                              onClick={handleErrorClose}
                              role="button"
                              aria-label="Close error message"
                              style={{ cursor: "pointer" }}
                            ></i>
                          </div>
                        </div>
                      )}
                      <div className="py-3">
                        <div className="form-group">
                          <input
                            type="text"
                            className="form-control form-control-lg form-control-alt"
                            id="username"
                            name="username"
                            placeholder="Username"
                            onChange={(e) => setUsername(e.target.value)}
                          />
                        </div>
                        <div className="form-group">
                          <input
                            type="password"
                            className="form-control form-control-lg form-control-alt"
                            id="login-password"
                            name="login-password"
                            placeholder="Password"
                            onChange={(e) => setPassword(e.target.value)}
                          />
                        </div>
                      </div>
                      <div className="form-group">
                        <button
                          type="submit"
                          className="btn btn-block btn-hero-lg btn-hero-primary"
                          onClick={handleSubmit}
                        >
                          <i className="fa fa-fw fa-sign-in-alt mr-1"></i> Sign
                          In
                        </button>
                        <p className="mt-3 mb-0 d-lg-flex justify-content-lg-between">
                          <a
                            className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
                            href="op_auth_reminder.html"
                          >
                            <i className="fa fa-exclamation-triangle text-muted mr-1"></i>{" "}
                            Forgot password
                          </a>
                          <Link
                            to="/sign_up"
                            className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
                          >
                            <i className="fa fa-plus text-muted mr-1"></i> New
                            Account
                          </Link>
                        </p>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </div>
            <div className="hero-static col-md-6 d-none d-md-flex align-items-md-center justify-content-md-center text-md-center">
              <div className="p-3">
                <p className="display-4 font-w700 text-white mb-3">
                  Welcome to the future
                </p>
                <p className="font-size-lg font-w600 text-white-75 mb-0">
                  Copyright &copy; <span className="js-year-copy">2018</span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default SignIn;
