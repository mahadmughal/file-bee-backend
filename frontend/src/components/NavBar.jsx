import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <div className='page_container'>
      <header className='page-header'>
        <div className="bg-white p-3 rounded push">
          <div id="horizontal-navigation-hover-centered" className="d-none d-lg-block mt-2 mt-lg-0">
            <ul className="nav-main nav-main-horizontal nav-main-hover nav-main-horizontal-center">
              <li className="nav-main-item">
                <a className="nav-main-link active" href="be_ui_navigation_horizontal.html">
                  <i className="nav-main-link-icon fa fa-rocket"></i>
                  <span className="nav-main-link-name">Overview</span>
                  <span className="nav-main-link-badge badge badge-pill badge-success">3</span>
                </a>
              </li>
              <li className="nav-main-heading">Manage</li>
              <li className="nav-main-item">
                <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                  <i className="nav-main-link-icon fa fa-boxes"></i>
                  <span className="nav-main-link-name">Products</span>
                </a>
                <ul className="nav-main-submenu">
                  <li className="nav-main-item">
                    <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                      <i className="nav-main-link-icon fab fa-wordpress"></i>
                      <span className="nav-main-link-name">WordPress Theme</span>
                    </a>
                    <ul className="nav-main-submenu">
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-pencil-alt"></i>
                          <span className="nav-main-link-name">Description</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-pie"></i>
                          <span className="nav-main-link-name">Statistics</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-line"></i>
                          <span className="nav-main-link-name">Sales</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">260</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-image"></i>
                          <span className="nav-main-link-name">Media</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">2</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-file"></i>
                          <span className="nav-main-link-name">Files</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">3</span>
                        </a>
                      </li>
                    </ul>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                      <i className="nav-main-link-icon fa fa-code"></i>
                      <span className="nav-main-link-name">HTML Template</span>
                    </a>
                    <ul className="nav-main-submenu">
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-pencil-alt"></i>
                          <span className="nav-main-link-name">Description</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-pie"></i>
                          <span className="nav-main-link-name">Statistics</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-line"></i>
                          <span className="nav-main-link-name">Sales</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">741</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-image"></i>
                          <span className="nav-main-link-name">Media</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">5</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-file"></i>
                          <span className="nav-main-link-name">Files</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">1</span>
                        </a>
                      </li>
                    </ul>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                      <i className="nav-main-link-icon fab fa-youtube-square"></i>
                      <span className="nav-main-link-name">Video Template</span>
                    </a>
                    <ul className="nav-main-submenu">
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-pencil-alt"></i>
                          <span className="nav-main-link-name">Description</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-pie"></i>
                          <span className="nav-main-link-name">Statistics</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-line"></i>
                          <span className="nav-main-link-name">Sales</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">820</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-image"></i>
                          <span className="nav-main-link-name">Media</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">4</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-file"></i>
                          <span className="nav-main-link-name">Files</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">1</span>
                        </a>
                      </li>
                    </ul>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                      <i className="nav-main-link-icon fab fa-app-store"></i>
                      <span className="nav-main-link-name">Web Application</span>
                    </a>
                    <ul className="nav-main-submenu">
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-pencil-alt"></i>
                          <span className="nav-main-link-name">Description</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-pie"></i>
                          <span className="nav-main-link-name">Statistics</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon fa fa-chart-line"></i>
                          <span className="nav-main-link-name">Sales</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">150</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-image"></i>
                          <span className="nav-main-link-name">Media</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">3</span>
                        </a>
                      </li>
                      <li className="nav-main-item">
                        <a className="nav-main-link" href="javascript:void(0)">
                          <i className="nav-main-link-icon far fa-file"></i>
                          <span className="nav-main-link-name">Files</span>
                          <span className="nav-main-link-badge badge badge-pill badge-primary">2</span>
                        </a>
                      </li>
                    </ul>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <i className="nav-main-link-icon fa fa-plus-circle"></i>
                      <span className="nav-main-link-name">New Product</span>
                    </a>
                  </li>
                </ul>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                  <i className="nav-main-link-icon fa fa-money-bill"></i>
                  <span className="nav-main-link-name">Payments</span>
                </a>
                <ul className="nav-main-submenu">
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Scheduled</span>
                      <span className="nav-main-link-badge badge badge-pill badge-success">2</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Recurring</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Manage</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <i className="nav-main-link-icon fa fa-plus-circle"></i>
                      <span className="nav-main-link-name">New Payment</span>
                    </a>
                  </li>
                </ul>
              </li>
              <li className="nav-main-item">
                <a className="nav-main-link nav-main-link-submenu" data-toggle="submenu" aria-haspopup="true" aria-expanded="false" href="#">
                  <i className="nav-main-link-icon fa fa-globe"></i>
                  <span className="nav-main-link-name">Services</span>
                </a>
                <ul className="nav-main-submenu">
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Hosting</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Web Design</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Web Development</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Graphic Design</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Legal</span>
                    </a>
                  </li>
                  <li className="nav-main-item">
                    <a className="nav-main-link" href="javascript:void(0)">
                      <span className="nav-main-link-name">Consulting</span>
                    </a>
                  </li>
                </ul>
              </li>
              <li className="nav-main-heading">Personal</li>
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
