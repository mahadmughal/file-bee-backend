import React from "react";
import { useState } from "react";
import { Link } from "react-router-dom";
import Alert from "./Alert";

function RequestPasswordResetToken() {
  const [email, setEmail] = useState("");
  const [alert, setAlert] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      setAlert({
        message: "Email is required to reset password",
        type: "danger",
      });
      return;
    }

    const url = "http://localhost:8000/api/user/request_reset_password/";
    const header = { "X-CSRFTOKEN": getCookie("csrftoken") };
    const formData = new FormData();
    formData.append("email", email);

    try {
      const response = await fetch(url, {
        method: "POST",
        header,
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        setAlert({
          message: errorData?.error || "Password reset failed",
          type: "danger",
        });
      } else {
        console.log("Password reset successful:", response);
        setAlert({
          message: "You will receive confirmation email to reset your password",
          type: "success",
        });
      }
    } catch (error) {
      setAlert({ message: error.toString(), type: "danger" });
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

  return (
    <form
      className="js-validation-reminder"
      action="be_pages_auth_all.html"
      method="POST"
    >
      {alert?.message && <Alert alert={alert} />}
      <div className="form-group py-3">
        <input
          type="text"
          className="form-control form-control-lg form-control-alt"
          id="reminder-credential"
          name="reminder-credential"
          placeholder="Username or Email"
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className="form-group text-center">
        <button
          type="submit"
          className="btn btn-block btn-hero-lg btn-hero-warning"
          onClick={handleSubmit}
        >
          <i className="fa fa-fw fa-reply mr-1"></i> Reset Password
        </button>
        <p className="mt-3 mb-0 d-lg-flex justify-content-lg-between">
          <Link
            to="/sign_in"
            className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
          >
            <i className="fa fa-sign-in-alt text-muted mr-1"></i>
            Sign In
          </Link>
          <Link
            to="/sign_up"
            className="btn btn-sm btn-light d-block d-lg-inline-block mb-1"
          >
            <i className="fa fa-plus text-muted mr-1"></i>
            New Account
          </Link>
        </p>
      </div>
    </form>
  );
}

export default RequestPasswordResetToken;
