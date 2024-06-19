import React from "react";
import { useParams } from "react-router-dom";
import bgImage from "../../assets/images/photo5@2x.jpg";
import RequestpPasswordResetToken from "../../components/RequestPasswordResetToken";
import ChangePassword from "../../components/ChangePassword";

function ResetPassword() {
  const { token } = useParams();

  return (
    <div id="page-container">
      <main id="main-container">
        <div
          className="bg-image"
          style={{ backgroundImage: `url(${bgImage})` }}
        >
          <div className="row no-gutters bg-gd-sun-op">
            <div className="hero-static col-md-6 d-flex align-items-center bg-white">
              <div className="p-3 w-100">
                <div className="text-center">
                  <a
                    className="link-fx text-warning font-w700 font-size-h1"
                    href="index.html"
                  >
                    <span className="text-dark">File</span>
                    <span className="text-warning">Bee</span>
                  </a>
                  <p className="text-uppercase font-w700 font-size-sm text-muted">
                    Password {token ? "Reset" : "Reminder"}
                  </p>
                </div>

                <div className="row no-gutters justify-content-center">
                  <div className="col-sm-8 col-xl-6">
                    {token ? (
                      <ChangePassword passwordResetToken={token} />
                    ) : (
                      <RequestpPasswordResetToken />
                    )}
                  </div>
                </div>
              </div>
            </div>
            <div className="hero-static col-md-6 d-none d-md-flex align-items-md-center justify-content-md-center text-md-center">
              <div className="p-3">
                <p className="display-4 font-w700 text-white mb-0">
                  Don’t worry of failure..
                </p>
                <p className="font-size-h1 font-w600 text-white-75 mb-0">
                  ..but learn from it!
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ResetPassword;
