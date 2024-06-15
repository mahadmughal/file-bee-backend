import React from "react";
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <div className="page_container">
      <header className="page-header">
        <div className="bg-white p-3 rounded push">
          <div
            id="horizontal-navigation-hover-centered"
            className="d-none d-lg-block mt-2 mt-lg-0"
          >
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
                <ul className="nav-main-submenu">
                  <li className="nav-main-item">
                    <Link to="/image_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-images"></i>
                      <span className="nav-main-link-name">Image Converter</span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link to="/document_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-file"></i>
                      <span className="nav-main-link-name">Document Converter</span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link to="/audio_converter" className="nav-main-link">
                      <i className="nav-main-link-icon fa fa-file-audio"></i>
                      <span className="nav-main-link-name">Audio Converter</span>
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
        </div>
      </header>
    </div>
  );
};

export default NavBar;
