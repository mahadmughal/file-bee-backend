import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <div className="page_container">
      <header className="page-header">
        <div className="bg-white p-3 rounded push row text-center justify-content-around">
          <div className="col-3">
            <Link to="/" className="link-fx font-w700 font-size-h1">
              <span className="text-dark">File</span>
              <span className="text-primary">Bee</span>
            </Link>
          </div>
          <div id="horizontal-navigation-hover-centered" className="col-6">
            <ul className="nav-main nav-main-horizontal nav-main-hover nav-main-horizontal-center">
              <li className="nav-main-item">
                <a
                  className="nav-main-link active"
                  href="be_ui_navigation_horizontal.html"
                >
                  <i className="nav-main-link-icon fa fa-rocket"></i>
                  <span className="nav-main-link-name">Overview</span>
                </a>
              </li>
              <li className="nav-main-item">
                <a
                  className="nav-main-link nav-main-link-submenu"
                  data-toggle="submenu"
                  aria-haspopup="true"
                  aria-expanded="false"
                  href="#"
                >
                  <i className="nav-main-link-icon fa fa-boxes"></i>
                  <span className="nav-main-link-name">Converters</span>
                </a>
                <ul className="nav-main-submenu text-left">
                  <li className="nav-main-item">
                    <Link to="/image_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-images"></i>
                      <span className="nav-main-link-name">
                        Image Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link to="/document_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-file"></i>
                      <span className="nav-main-link-name">
                        Document Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link to="/audio_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-file-audio"></i>
                      <span className="nav-main-link-name">
                        Audio Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link to="/font_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-font"></i>
                      <span className="nav-main-link-name">Font Converter</span>
                    </Link>
                  </li>
                </ul>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link" href="#">
                  <i className="nav-main-link-icon fa fa-money-bill"></i>
                  <span className="nav-main-link-name">Pricing</span>
                </a>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link" href="javascript:void(0)">
                  <i className="nav-main-link-icon far fa-user-circle"></i>
                  <span className="nav-main-link-name">Profile</span>
                </a>
              </li>
            </ul>
          </div>
          <div className="col-3 mt-2">
            <Link
              to="/sign_in"
              className="btn btn-outline-primary mr-1"
              type="button"
            >
              Log in
            </Link>
            <Link to="/sign_up" className="btn btn-primary" type="button">
              Sign up
            </Link>
          </div>
        </div>
      </header>
    </div>
  );
};

export default NavBar;
