import React, { Component, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";

const FormChildren = (props) => {
  return (
    <Form.Group className="mb-3">
      <Form.Label>{props.header}</Form.Label>
      <Form.Control
        type="text"
        placeholder={props.example}
        id={props.idname}
        name={props.idname}
        value={props.value}
        onChange={(event) => props.changeValue(event.target.value)}
        autoComplete="off"
      />
    </Form.Group>
  );
};

export default FormChildren;
