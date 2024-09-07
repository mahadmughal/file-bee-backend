import React from "react";
import bgImage from "../assets/images/help.png";
import { Link } from "react-router-dom";

const Help = () => {
  return (
    <main id="main-container">
      <div className="content content-boxed">
        <div className="row align-items-center pt-5">
          <div className="col-md-6 order-md-1 text-center text-md-left">
            <h1 className="h2 mb-4">How can we help?</h1>
            <p className="font-size-lg font-w400 text-muted mb-4 pr-5">
              We offer the most complete support to our customers. We are here
              for your service.
            </p>
            <Link
              to="/help/submit_request"
              className="btn btn-hero btn-primary"
            >
              Submit a request
            </Link>
          </div>
          <div className="col-md-6 order-md-2 text-center mb-5 mb-md-0">
            <img
              src={bgImage}
              alt="Help"
              className="img-fluid rounded shadow-lg"
              style={{ maxWidth: "100%", height: "auto" }}
            />
          </div>
        </div>
      </div>
    </main>
  );
};

export default Help;
