import React from "react";
import logo from "../assets/logo.png";
import { FaBluetooth } from "react-icons/fa";

const Header: React.FC = () => {
  return (
    <header className="d-flex align-items-center justify-content-center px-4">
      <img src={logo} alt="House Music Logo" width="55px" />
      <div className="bluetooth-device position-absolute top-0 start-0 p-3 d-flex align-items-center">
        <FaBluetooth/>
        <div id="bluetooth-device-status" className="d-inline ms-2" style={{ fontSize: "13px" }}>
          <div className="loader"></div>
        </div>
      </div>
    </header>
  );
};

export default Header;
