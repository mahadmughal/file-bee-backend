import React from "react";
import { Link } from "react-router-dom";
import bgImage from "../assets/images/photo5@2x.jpg";

const ComingSoon = () => {
  return (
    <main id="main-container">
      <div className="bg-image" style={{ backgroundImage: `url(${bgImage})` }}>
        <div className="hero bg-black-25">
          <div className="hero-inner">
            <div className="content content-full">
              <div className="row justify-content-center">
                <div className="col-md-6 col-xl-4 py-5 text-center bg-black-75 rounded">
                  <div className="push border-bottom border-white-op">
                    <Link className="link-fx font-w700 font-size-h1" to="/">
                      <span className="text-white">File</span>
                      <span className="text-primary">Bee</span>
                    </Link>
                    <p className="text-uppercase font-w700 font-size-sm text-white-75">
                      Stay tuned, it is coming soon
                    </p>
                  </div>
                  <Link className="btn btn-hero-sm btn-hero-primary" to="/">
                    <i className="fa fa-arrow-left mr-1"></i> Go Back
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default ComingSoon;
