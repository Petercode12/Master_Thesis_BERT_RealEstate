import React from "react";
import Translate from "react-translate-component";
import { Row, Col, Nav, Navbar } from "react-bootstrap";
import "../Style/Navigation.css";
import counterpart from "counterpart";
import en from "../lang/en";
import { Link } from "react-router-dom";

counterpart.registerTranslations("en", en);

class Navigation extends React.Component {
  render() {
    return (
      <Navbar collapseOnSelect expand="lg">
        <Navbar.Brand />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="navigation">
            <Row>
              <Col xl={12} style={{ padding: 0 }}>
                <Link to="/" style={{ textDecoration: "none" }}>
                  <p className="text-semi-bold first-element">
                    <Translate content="navigation.title" />
                  </p>
                </Link>
                <Link to="/insertData" style={{ textDecoration: "none" }}>
                  <p> Insert</p>
                </Link>
                <Link to="/chart" style={{ textDecoration: "none" }}>
                  <p> Chart</p>
                </Link>
              </Col>
            </Row>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
    );
  }
}

export default Navigation;
