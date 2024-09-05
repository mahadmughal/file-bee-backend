import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const NavBar = () => {
  const location = useLocation();
  const auth = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [activeLink, setActiveLink] = useState(location.pathname);

  const handleNavLinkClick = (path) => {
    setActiveLink(path);
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const isActive = (path) => {
    return activeLink === path ? "active" : "";
  };

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
                <Link
                  to="/"
                  className={`nav-main-link ${isActive("/")}`}
                  onClick={() => handleNavLinkClick("/")}
                >
                  <i className="nav-main-link-icon fa fa-compass"></i>
                  <span className="nav-main-link-name">Overview</span>
                </Link>
              </li>
              <li className="nav-main-item">
                <a
                  className={`nav-main-link ${
                    activeLink.includes("_converter") ? "active" : ""
                  } nav-main-link-submenu`}
                  data-toggle="submenu"
                  aria-haspopup="true"
                  aria-expanded="false"
                  href="#"
                >
                  <i className="nav-main-link-icon fa fa-redo fa-spin text-primary"></i>
                  <span className="nav-main-link-name">Converters</span>
                </a>
                <ul className="nav-main-submenu text-left">
                  <li className="nav-main-item">
                    <Link
                      to="/image_converter"
                      className={`nav-main-link ${isActive(
                        "/image_converter"
                      )}`}
                      onClick={() => handleNavLinkClick("/image_converter")}
                    >
                      <i className="nav-main-link-icon fa fa-images"></i>
                      <span className="nav-main-link-name">
                        Image Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link
                      to="/document_converter"
                      className={`nav-main-link ${isActive(
                        "/document_converter"
                      )}`}
                      onClick={() => handleNavLinkClick("/document_converter")}
                    >
                      <i className="nav-main-link-icon fa fa-file"></i>
                      <span className="nav-main-link-name">
                        Document Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link
                      to="/audio_converter"
                      className={`nav-main-link ${isActive(
                        "/audio_converter"
                      )}`}
                      onClick={() => handleNavLinkClick("/audio_converter")}
                    >
                      <i className="nav-main-link-icon fa fa-file-audio"></i>
                      <span className="nav-main-link-name">
                        Audio Converter
                      </span>
                    </Link>
                  </li>
                  <li className="nav-main-item">
                    <Link
                      to="/font_converter"
                      className={`nav-main-link ${isActive("/font_converter")}`}
                      onClick={() => handleNavLinkClick("/font_converter")}
                    >
                      <i className="nav-main-link-icon fa fa-font"></i>
                      <span className="nav-main-link-name">Font Converter</span>
                    </Link>
                  </li>
                </ul>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link" href="#">
                  <i className="nav-main-link-icon fa fa-fw fa-magic"></i>
                  <span className="nav-main-link-name">API</span>
                </a>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link" href="javascript:void(0)">
                  <i className="nav-main-link-icon fa fa-hands-helping"></i>
                  <span className="nav-main-link-name">Help</span>
                </a>
              </li>
            </ul>
          </div>
          <div className="col-3 mt-2">
            {!auth.token ? (
              <>
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
              </>
            ) : (
              <>
                <button
                  type="button"
                  className="btn btn-dual"
                  id="page-header-user-dropdown"
                  data-toggle="dropdown"
                  onClick={toggleDropdown}
                >
                  <i className="far fa-user"></i>
                  <i className="fa fa-fw fa-angle-down ml-1 d-none d-sm-inline-block"></i>
                </button>
                {isOpen && (
                  <div
                    className="dropdown-menu"
                    aria-labelledby="page-header-user-dropdown"
                  >
                    <div class="bg-primary-darker rounded-top font-w600 text-white text-center p-3">
                      {auth.user?.username || "User options"}
                    </div>
                    <div className="p-2">
                      <Link className="dropdown-item" to="/profile">
                        <i className="far fa-fw fa-user mr-1"></i> Profile
                      </Link>
                      <div role="separator" className="dropdown-divider"></div>
                      <a
                        className="dropdown-item"
                        href="javascript:void(0)"
                        data-toggle="layout"
                        data-action="side_overlay_toggle"
                      >
                        <i className="far fa-fw fa-building mr-1"></i> Settings
                      </a>
                      <div role="separator" className="dropdown-divider"></div>
                      <Link
                        to="/sign_in"
                        className="dropdown-item"
                        onClick={(e) => {
                          e.preventDefault();
                          auth.logOut();
                        }}
                      >
                        <i className="far fa-fw fa-arrow-alt-circle-left mr-1"></i>
                        Sign Out
                      </Link>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </header>
    </div>
  );
};

export default NavBar;
