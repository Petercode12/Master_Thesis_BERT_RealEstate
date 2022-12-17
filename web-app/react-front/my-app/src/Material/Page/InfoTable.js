import React, { useState, useEffect, useContext } from "react";
import "../Style/houseList.css";
import "react-pagination-bar/dist/index.css";
import { Button, Col, Form, FormCheck, Nav, Row, Table } from "react-bootstrap";
import axios from "axios";
import ReactPaginate from "react-paginate";
import { langContext } from "../App.js";
import en from "../lang/en.js";
import Translate from "react-translate-component";
import "../Style/PopUpBox.css";

function deleteProject(house) {
  const delete_content = {
    id: house[0],
  };
  console.log(delete_content);
  axios({
    url: "http://127.0.0.1:8000/delete/house",
    method: "POST",
    params: delete_content,
  })
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.error("Wasn't able to delete property.", err);
      alert("Cannot delete! The house does not exist");
    });
}

export default function InfoTable() {
  const [posts, setPosts] = useState([]);
  const [tempPosts, setTempPosts] = useState([]);
  const [postsDel, setPostsDel] = useState([]);
  const [itemOffset, setItemOffset] = useState(0);
  const { lang, setLang } = useContext(langContext);
  const [loadingPopUp, setLoadingPopUp] = useState("block");
  const [loadingPopUp2, setLoadingPopUp2] = useState("none");
  const [logicalOperator, setLogicalOperator] = useState("AND");
  const [queryTime, setQueryTime] = useState(0);
  useEffect(() => {
    axios({
      url: "http://127.0.0.1:8000/getAllData/",
      method: "GET",
    })
      .then((res) => {
        console.log(res);
        setLoadingPopUp("none");
        setPosts(res.data);
        setTempPosts(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  console.log(posts);
  const pagePostsLimit = 8;

  // Delete rows functions
  const removeElementById = (id) => {
    const postsAfterRemove = posts.filter((post) => post[0] !== id);
    setPosts(postsAfterRemove);
  };
  const removeElementsById = (ids) => {
    const postsAfterRemove = posts.filter((post) => !ids.includes(post[0]));
    setPostsDel([]);
    setPosts(postsAfterRemove);
  };
  const deleteBtn = (post) => {
    return (
      <button
        className="fa fa-trash"
        style={{
          color: "red",
          backgroundColor: "white",
          border: 0,
        }}
        onClick={() => {
          alert("You want to delete this row?");
          deleteProject(post);
          removeElementById(post[0]);
        }}
      ></button>
    );
  };

  // Filter functions
  const handleFilter = () => {
    setLoadingPopUp2("block");
    const area = document.getElementById("searchByArea").value;
    const compareArea = document.getElementById("compareArea").value;
    const floors = document.getElementById("searchByFloors").value;
    const compareFloors = document.getElementById("compareFloors").value;
    const address = document.getElementById("searchByAddress").value;
    const owner = document.getElementById("searchByOwner").value;
    console.log("Area: ", area);
    console.log("Compare Area: ", compareArea);
    console.log("Floors: ", floors);
    console.log("Compare Floors: ", compareFloors);
    console.log("Address: ", address);
    console.log("Owner: ", owner);
    console.log("Operator: ", logicalOperator);
    const search_content = {
      area: area,
      compareArea: compareArea,
      floors: floors,
      compareFloors: compareFloors,
      address: address,
      owner: owner,
      logicalOperator: logicalOperator,
    };
    axios({
      url: "http://127.0.0.1:8000/getSearchData/",
      method: "POST",
      params: search_content,
    })
      .then((res) => {
        console.log("Res: ", res);
        setLoadingPopUp2("none");
        setQueryTime(res.data[res.data.length - 1]);
        setPosts(res.data);
      })
      .catch((err) => {
        console.error("Wasn't able to select records.", err);
        alert("Cannot select records!");
      });
  };

  // Extra functions for handling features
  const checkedBoxCount = (post) => {
    const box = document.querySelectorAll(
      ".house".concat(post[0].toString()).concat(" .form-check-input")
    )[0];
    console.log(box);
    console.log(box.checked);
    if (box.checked) {
      setPostsDel([...postsDel, post]);
    } else {
      setPostsDel(postsDel.filter((p) => p[0] !== post[0]));
    }
  };

  const handlePageClick = (event) => {
    const newOffset = (event.selected * pagePostsLimit) % posts.length;
    console.log(
      `User requested page number ${event.selected}, which is offset ${newOffset}`
    );
    setItemOffset(newOffset);
  };

  const switchArrow = () => {
    const arrow = document.getElementById("arrow");
    if (arrow.className === "fa fa-angle-up") {
      arrow.className = "fa fa-angle-down";
    } else {
      arrow.className = "fa fa-angle-up";
    }
    setPosts([
      ...posts.sort(function (a, b) {
        if (arrow.className === "fa fa-angle-up") {
          return a[9].localeCompare(b[9]);
        } else {
          return b[9].localeCompare(a[9]);
        }
      }),
    ]);
  };

  return (
    <div>
      <h2 style={{ marginTop: "1em" }}>
        <Translate content="houseList.title" />
      </h2>
      <hr />
      <div>
        <Form className="filterForm">
          <Form.Group as={Row} className="mb-3">
            <Col sm="3">
              <Form.Control
                type="text"
                id="searchByArea"
                placeholder={lang === en ? "Area" : "Numéro de projet, nom"}
                style={{ marginTop: "4px" }}
              />
            </Col>
            <Col sm="3">
              <Form.Control
                type="text"
                as="select"
                id="compareArea"
                defaultValue="select type"
                style={{ marginTop: "4px" }}
              >
                <option value="select type">
                  {lang === en ? "Comparison" : "L'état du projet"}
                </option>
                <option value=">">&gt;</option>
                <option value="<">&lt;</option>
                <option value="<=">&le;</option>
                <option value=">=">&ge;</option>
                <option value="=">&#61;</option>
              </Form.Control>
            </Col>
            <Button
              as="input"
              variant="primary"
              type="button"
              id="searchBtn"
              value={lang === en ? "Search" : "Rechercher un projet"}
              onClick={() => {
                handleFilter();
              }}
            ></Button>
            <Button
              as="input"
              variant="secondary"
              type="button"
              id="resetBtn"
              value={
                lang === en ? "Reset Search" : "Réinitialiser la recherche"
              }
              onClick={() => {
                window.location.reload();
              }}
            ></Button>
          </Form.Group>

          <Form.Group as={Row} className="mb-3">
            <Col sm="3">
              <Form.Control
                type="text"
                id="searchByFloors"
                placeholder={lang === en ? "Floors" : "Numéro de projet, nom"}
              />
            </Col>
            <Col sm="3">
              <Form.Control
                type="text"
                as="select"
                id="compareFloors"
                defaultValue="select license"
              >
                <option value="select license">
                  {lang === en ? "Comparison" : "L'état du projet"}
                </option>
                <option value=">">&gt;</option>
                <option value="<">&lt;</option>
                <option value="<=">&le;</option>
                <option value=">=">&ge;</option>
                <option value="=">&#61;</option>
              </Form.Control>
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Col sm="3">
              <Form.Control
                type="text"
                id="searchByAddress"
                placeholder={lang === en ? "Address" : "Numéro de projet, nom"}
              />
            </Col>
            <Col sm="3">
              Logical Operators:
              <Form.Check
                inline
                value="AND"
                type="radio"
                id="And"
                name="radioGroup"
                label="And"
                onChange={() => {
                  setLogicalOperator("AND");
                }}
                style={{ marginLeft: "10px" }}
              />
              <Form.Check
                inline
                value="OR"
                type="radio"
                id="Or"
                name="radioGroup"
                label="Or"
                onChange={() => {
                  setLogicalOperator("OR");
                }}
              />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Col sm="3">
              <Form.Control
                type="text"
                id="searchByOwner"
                placeholder={lang === en ? "Owner" : "Numéro de projet, nom"}
              />
            </Col>
            <Col sm="3">
              <p>Query time: {queryTime} s</p>
            </Col>
          </Form.Group>
        </Form>
      </div>
      <div style={{ minHeight: "509px" }}>
        <Table responsive>
          <thead>
            <tr>
              <th> </th>
              <th>ID</th>
              <th>
                <Translate content="houseList.address" />{" "}
                <button
                  className="fa fa-angle-up"
                  id="arrow"
                  style={{ backgroundColor: "white", border: "0" }}
                  onClick={switchArrow}
                ></button>
              </th>
              <th>
                <Translate content="houseList.owner" />
              </th>
              <th>
                <Translate content="houseList.unit_price" />
              </th>
              <th>
                <Translate content="houseList.area" />
              </th>
              <th>
                <Translate content="houseList.floors" />
              </th>
              <th>
                <Translate content="houseList.delete" />
              </th>
            </tr>
          </thead>
          <tbody id="tableBody">
            {posts
              .slice(itemOffset, itemOffset + pagePostsLimit)
              .map((post) => {
                return (
                  <tr key={post[0]}>
                    <td>
                      <Form>
                        <FormCheck
                          className={"house".concat(post[0])}
                          id={post[0]}
                          onClick={() => {
                            checkedBoxCount(post);
                          }}
                        />
                      </Form>
                    </td>
                    <td>
                      <Nav.Link style={{ color: "blue" }} href={`\\${post[0]}`}>
                        {post[0]}
                      </Nav.Link>
                    </td>
                    <td>{post[9]}</td>
                    <td>{post[2]}</td>
                    <td>{post[4]}</td>
                    <td>{post[10]}</td>
                    <td>{post[7]}</td>
                    <td>{deleteBtn(post)}</td>
                  </tr>
                );
              })}
            <tr>
              <td
                colSpan="3"
                style={{ textAlign: "left", color: "blue" }}
                id="numOfSelected"
              >
                {postsDel.length}{" "}
                {lang === en ? "items selected" : "éléments sélectionnés"}
              </td>
              <td colSpan="7" style={{ textAlign: "right", color: "red" }}>
                <button
                  style={{
                    color: "red",
                    backgroundColor: "white",
                    border: 0,
                  }}
                  onClick={() => {
                    let ids = [];
                    alert("You want to delete these rows?");
                    for (const house of postsDel) {
                      ids.push(house[0]);
                      deleteProject(house);
                    }
                    removeElementsById(ids);
                  }}
                >
                  {lang === en
                    ? "delete selected items"
                    : "supprimer les éléments sélectionnés"}{" "}
                  <i className="fa fa-trash"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </Table>
      </div>
      <div
        style={{ float: "right", marginRight: "18px", marginBottom: "19px" }}
      >
        <ReactPaginate
          nextLabel={lang === en ? "next >" : "> suivant"}
          onPageChange={handlePageClick}
          pageRangeDisplayed={3}
          marginPagesDisplayed={2}
          pageCount={Math.ceil(posts.length / pagePostsLimit)}
          previousLabel={lang === en ? "< previous" : "< précédente"}
          pageClassName="page-item"
          pageLinkClassName="page-link"
          previousClassName="page-item"
          previousLinkClassName="page-link"
          nextClassName="page-item"
          nextLinkClassName="page-link"
          breakLabel="..."
          breakClassName="page-item"
          breakLinkClassName="page-link"
          containerClassName="pagination"
          activeClassName="active"
          renderOnZeroPageCount={null}
        />
      </div>
      <div className="overlay" style={{ display: loadingPopUp }}>
        <div className="popup">
          <h2>
            Loading data{" "}
            <i
              style={{ marginLeft: "3px" }}
              className="fa fa-spinner fa-spin"
            ></i>
          </h2>
          <div className="content">Please wait a min!</div>
        </div>
      </div>
      <div className="overlay" style={{ display: loadingPopUp2 }}>
        <div className="popup">
          <h2>
            Loading data{" "}
            <i
              style={{ marginLeft: "3px" }}
              className="fa fa-spinner fa-spin"
            ></i>
          </h2>
          <div className="content">Please wait a min!</div>
        </div>
      </div>
    </div>
  );
}
