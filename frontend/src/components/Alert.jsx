import React from "react";
import "../App.css";

const AlertComponent = ({ type = "info", title, message, onClose }) => {
  const getAlertClass = () => {
    switch (type) {
      case "success":
        return "alert-success";
      case "error":
        return "alert-danger";
      case "warning":
        return "alert-warning";
      default:
        return "alert-info";
    }
  };

  return (
    <div
      className={`alert ${getAlertClass()} alert-dismissible fade show`}
      role="alert"
    >
      {title && <strong>{title}</strong>}
      {title && message && " "} {message}
      {onClose && (
        <button
          type="button"
          className="close"
          data-dismiss="alert"
          aria-label="Close"
          onClick={onClose}
        ></button>
      )}
    </div>
  );
};

export default AlertComponent;
