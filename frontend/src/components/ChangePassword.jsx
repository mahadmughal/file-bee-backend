import React from "react";
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Alert from "./Alert";
import { useApiService } from "../services/apiService";

function ChangePassword({ passwordResetToken }) {
  const apiService = useApiService();

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [alert, setAlert] = useState({});

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!newPassword) {
      setAlert({ message: "Please enter your password", type: "danger" });
      return;
    }

    if (newPassword !== confirmPassword) {
      setAlert({ message: "Passwords do not match", type: "danger" });
      return;
    }

    try {
      const response = await apiService.resetPassword(
        passwordResetToken,
        newPassword,
        confirmPassword
      );

      console.log("Password changed successfully:", response);
      setAlert({ message: "Password Changed successfully", type: "success" });
      navigate("/sign_in");
    } catch (error) {
      setAlert({
        message: error.message || "Password reset failed",
        type: "danger",
      });
      console.error("Reset password error: ", error);
    }
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
          id="new-password"
          name="new-password"
          placeholder="New password"
          onChange={(e) => setNewPassword(e.target.value)}
        />
      </div>
      <div className="form-group py-3">
        <input
          type="text"
          className="form-control form-control-lg form-control-alt"
          id="confirm-password"
          name="confirm-password"
          placeholder="Confirm password"
          onChange={(e) => setConfirmPassword(e.target.value)}
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

export default ChangePassword;
