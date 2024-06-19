import React from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import bgImage from "../../assets/images/photo22@2x.jpg";

function SignUp() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState(""); // Added email field
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(null); // State for error handling
  const [termsAccepted, setTermsAccepted] = useState(false); // State for terms acceptance

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic form validation (optional, consider using a library)
    if (!username) {
      setError("Username is required");
      return;
    }

    if (!email) {
      setError("Email is required");
      return;
    }

    if (password.length < 8) {
      setError("Password should be of minimum 8 characters");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (!termsAccepted) {
      setError("Please accept the Terms & Conditions");
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/api/user/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Set appropriate header
        },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        setError(errorData.error || "Registration failed");
        console.log("Registration failed:", response);
      } else {
        console.log("User registration successful:", response);
        navigate("/sign_in");
      }
    } catch (error) {
      setError("An error occurred. Please try again later.");
    }
  };

  const handleTermsChange = (e) => {
    setTermsAccepted(e.target.checked);
  };

  const handleErrorClose = (e) => {
    setError(null);
  };

  return (
    <>
      <div id="page-container">
        <main id="main-container">
          <div
            className="bg-image"
            style={{ backgroundImage: `url(${bgImage})` }}
          >
            <div className="row no-gutters justify-content-center bg-black-75">
              <div className="hero-static col-md-6 d-flex align-items-center bg-white">
                <div className="p-3 w-100">
                  <div className="mb-3 text-center">
                    <Link
                      to="/"
                      className="link-fx text-success font-w700 font-size-h1"
                    >
                      <span className="text-dark">File</span>
                      <span className="text-success">Bee</span>
                    </Link>
                    <p className="text-uppercase font-w700 font-size-sm text-muted">
                      Create New Account
                    </p>
                  </div>
                  <div className="row no-gutters justify-content-center">
                    <div className="col-sm-8 col-xl-6">
                      <form
                        className="js-validation-signup"
                        action="be_pages_auth_all.html"
                        method="POST"
                        onSubmit={handleSubmit} // Use onSubmit for form submission
                      >
                        {error && (
                          <div
                            className="alert alert-danger d-flex align-items-center justify-content-between"
                            role="alert"
                          >
                            <div className="flex-fill mr-3">
                              <p className="mb-0">{error}</p>
                            </div>
                            <div className="flex-00-auto">
                              <i
                                className="fa fa-fw fa-times-circle"
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
                              id="signup-username"
                              name="signup-username"
                              placeholder="Username"
                              onChange={(e) => setUsername(e.target.value)}
                            />
                          </div>
                          <div className="form-group">
                            <input
                              type="email"
                              className="form-control form-control-lg form-control-alt"
                              id="signup-email"
                              name="signup-email"
                              placeholder="Email"
                              onChange={(e) => setEmail(e.target.value)}
                            />
                          </div>
                          <div className="form-group">
                            <input
                              type="password"
                              className="form-control form-control-lg form-control-alt"
                              id="signup-password"
                              name="signup-password"
                              placeholder="Password"
                              onChange={(e) => setPassword(e.target.value)}
                            />
                          </div>
                          <div className="form-group">
                            <input
                              type="password"
                              className="form-control form-control-lg form-control-alt"
                              id="signup-password-confirm"
                              name="signup-password-confirm"
                              placeholder="Password Confirm"
                              onChange={(e) =>
                                setConfirmPassword(e.target.value)
                              }
                            />
                          </div>
                          <div className="form-group">
                            <div className="custom-control custom-checkbox custom-control-primary">
                              <input
                                type="checkbox"
                                className="custom-control-input"
                                id="signup-terms"
                                name="signup-terms"
                                checked={termsAccepted}
                                onChange={handleTermsChange}
                              />
                              <label
                                className="custom-control-label"
                                for="signup-terms"
                              >
                                I agree to Terms &amp; Conditions
                              </label>
                            </div>
                          </div>
                        </div>
                        <div className="form-group">
                          <button
                            type="submit"
                            className="btn btn-block btn-hero-lg btn-hero-success"
                          >
                            <i className="fa fa-fw fa-plus mr-1"></i> Sign Up
                          </button>
                          <p className="mt-3 mb-0 d-lg-flex justify-content-lg-between">
                            <Link
                              to="/sign_in"
                              className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
                            >
                              <i className="fa fa-sign-in-alt text-muted mr-1"></i>
                              Sign In
                            </Link>
                            <a
                              className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
                              href="#"
                              data-toggle="modal"
                              data-target="#modal-terms"
                            >
                              <i className="fa fa-book text-muted mr-1"></i>{" "}
                              Read Terms
                            </a>
                          </p>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
      <div
        className="modal fade"
        id="modal-terms"
        tabindex="-1"
        role="dialog"
        aria-labelledby="modal-terms"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-dialog-centered" role="document">
          <div className="modal-content">
            <div className="block block-themed block-transparent mb-0">
              <div className="block-header bg-primary-dark">
                <h3 className="block-title">Terms &amp; Conditions</h3>
                <div className="block-options">
                  <button
                    type="button"
                    className="btn-block-option"
                    data-dismiss="modal"
                    aria-label="Close"
                  >
                    <i className="fa fa-fw fa-times"></i>
                  </button>
                </div>
              </div>
              <div className="block-content">
                <p>
                  Dolor posuere proin blandit accumsan senectus netus nullam
                  curae, ornare laoreet adipiscing luctus mauris adipiscing
                  pretium eget fermentum, tristique lobortis est ut metus
                  lobortis tortor tincidunt himenaeos habitant quis dictumst
                  proin odio sagittis purus mi, nec taciti vestibulum quis in
                  sit varius lorem sit metus mi.
                </p>
                <p>
                  Dolor posuere proin blandit accumsan senectus netus nullam
                  curae, ornare laoreet adipiscing luctus mauris adipiscing
                  pretium eget fermentum, tristique lobortis est ut metus
                  lobortis tortor tincidunt himenaeos habitant quis dictumst
                  proin odio sagittis purus mi, nec taciti vestibulum quis in
                  sit varius lorem sit metus mi.
                </p>
                <p>
                  Dolor posuere proin blandit accumsan senectus netus nullam
                  curae, ornare laoreet adipiscing luctus mauris adipiscing
                  pretium eget fermentum, tristique lobortis est ut metus
                  lobortis tortor tincidunt himenaeos habitant quis dictumst
                  proin odio sagittis purus mi, nec taciti vestibulum quis in
                  sit varius lorem sit metus mi.
                </p>
                <p>
                  Dolor posuere proin blandit accumsan senectus netus nullam
                  curae, ornare laoreet adipiscing luctus mauris adipiscing
                  pretium eget fermentum, tristique lobortis est ut metus
                  lobortis tortor tincidunt himenaeos habitant quis dictumst
                  proin odio sagittis purus mi, nec taciti vestibulum quis in
                  sit varius lorem sit metus mi.
                </p>
                <p>
                  Dolor posuere proin blandit accumsan senectus netus nullam
                  curae, ornare laoreet adipiscing luctus mauris adipiscing
                  pretium eget fermentum, tristique lobortis est ut metus
                  lobortis tortor tincidunt himenaeos habitant quis dictumst
                  proin odio sagittis purus mi, nec taciti vestibulum quis in
                  sit varius lorem sit metus mi.
                </p>
              </div>
              <div className="block-content block-content-full text-right bg-light">
                <button
                  type="button"
                  className="btn btn-sm btn-primary"
                  data-dismiss="modal"
                >
                  Done
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default SignUp;
