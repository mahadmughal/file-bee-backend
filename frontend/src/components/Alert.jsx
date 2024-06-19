import React from "react";
import { useState } from "react";

function Alert({ alert }) {
  return (
    <div
      className={`alert alert-${alert?.type || "danger"} alert-dismissable`}
      role="alert"
    >
      <div className="flex-fill mr-3">
        <p className="mb-0">{alert?.message}</p>
      </div>
    </div>
  );
}

export default Alert;
