import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { Nav, Table } from "react-bootstrap";
function get_all_json_keys(json_object, ret_array = []) {
  for (const json_key in json_object) {
    if (
      typeof json_object[json_key] === "object" &&
      !Array.isArray(json_object[json_key])
    ) {
      ret_array.push(json_key);
      get_all_json_keys(json_object[json_key], ret_array);
    } else if (Array.isArray(json_object[json_key])) {
      ret_array.push(json_key);
      let first_element = json_object[json_key][0];
      if (typeof first_element === "object") {
        get_all_json_keys(first_element, ret_array);
      }
    } else {
      ret_array.push(json_key);
    }
  }

  return ret_array;
}

const generateElement = (key,value) => {
  return (
    <tr>
        <td>{key}</td>
        <td>{value}</td>
    </tr>
  );
}

function generateData(data) {
  const newData = Object.keys(data).reduce((result, currentKey) => {
    if (typeof data[currentKey] === 'string' || data[currentKey] instanceof String) {
      const elementToPush = generateElement(currentKey, data[currentKey]);
      result.push(elementToPush);
    } else {
      const nested = generateData(data[currentKey]);
      result.push(...nested);
    }
    return result;
  }, []);
  return newData;
}


export default function HouseDetail() {
  const [post, setPost] = useState({});
  const params = useParams();
  console.log("ID: ", params);
  useEffect(() => {
    axios({
      url: "http://127.0.0.1:8000/api/get-sentence?id=".concat(params.id),
      method: "GET",
    })
      .then((res) => {
        console.log(res);
        setPost(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);
  let all_keys = [];
  get_all_json_keys(post, all_keys);
  console.log("keys: ", all_keys);
  console.log("data: ", post[all_keys]);
  return (
    <div>
      <Nav.Link href="/" className="back">
        <p className="text-semi-bold first-element">
          <i className="fa fa-angle-left"></i> Back
        </p>
      </Nav.Link>
      <h2 style={{ marginTop: "0.5em" }}>
        Detail information of house with ID: {params.id}
      </h2>
      {post.house ? 
        <div>
          <Table responsive striped bordered>
            <tbody>
              {post.house.map((h) => {
                  return (
                    <tr>
                      <td><b>Raw data</b></td>
                      <td>{h.fields.Description}</td>
                  </tr>
                  );
                })}
            </tbody>
          </Table>
        </div>
        : null
      }
      {post.result_sentence ? 
        <div>
          <Table responsive striped bordered>
            <thead>
              <tr>
                <th>Label</th> <th>Content</th>
              </tr>
            </thead>
            <tbody>
             {generateData(post.result_sentence)}
            </tbody>
          </Table>
        </div>
        : null
      }
    </div>
  );
}
