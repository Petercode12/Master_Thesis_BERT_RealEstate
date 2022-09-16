import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import Header from "./Header";
import Navigation from "./Navigation";
import InfoTable from "./InfoTable";
import Login from "./Login";
import Register from "./Register";
import InsertData from "./InsertData";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Charts from "./Charts";
import Page404 from "./template/Page404";
import HouseDetail from "./HouseDetail";
function MainPage() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <Container fluid>
              <Row>
                <Col>
                  <Header />
                </Col>
              </Row>
              <Row>
                <Col xl={2}>
                  <Navigation />
                </Col>
                <Col xl={10}>
                  <InfoTable />
                </Col>
              </Row>
            </Container>
          }
        />
        <Route
          path="/insertData"
          element={
            <Container fluid>
              <Row>
                <Col>
                  <Header />
                </Col>
              </Row>
              <Row>
                <Col xl={2}>
                  <Navigation />
                </Col>
                <Col xl={10}>
                  <InsertData />
                </Col>
              </Row>
            </Container>
          }
        />
        <Route
          path="/chart"
          element={
            <Container fluid>
              <Row>
                <Col>
                  <Header />
                </Col>
              </Row>
              <Row>
                <Col xl={2}>
                  <Navigation />
                </Col>
                <Col xl={10}>
                  <Charts />
                </Col>
              </Row>
            </Container>
          }
        />
        <Route
          path="/:id"
          element={
            <Container fluid>
              <Row>
                <Col>
                  <Header />
                </Col>
              </Row>
              <Row>
                <Col xl={2}>
                  <Navigation />
                </Col>
                <Col xl={10}>
                  <HouseDetail />
                </Col>
              </Row>
            </Container>
          }
        />
        <Route path="*" element={<Page404 />} />
      </Routes>
    </BrowserRouter>
  );
}

export default MainPage;
