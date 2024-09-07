import React from "react";
import NavBar from "../components/NavBar";
import { Outlet } from "react-router-dom";

const Layout = ({ children }) => {
  return (
    <div>
      <NavBar />
      {children}
      <Outlet />
    </div>
  );
};

export default Layout;
