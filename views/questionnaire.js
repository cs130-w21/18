import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";
import PageHead from "../components/head";

const Questionnaire = (props) => {
  const [responses, setResponses] = useState(props.defaultSettings);

  return (
    <>
      <PageHead/>
      <div>
        <p>Tell us what kind of music you're in the mood for!</p>
      </div>
      <Form>
        <Form.Group controlId="formEnergyRange">
          <Form.Label>Energy</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0"
            max="10"
            step="1"
            defaultValue="5"
            onChange={(e) => setResponses({ energy: e.target.value })}
          />
        </Form.Group>
      </Form>
      <Button onClick={() => props.submitResponses(responses)}>Get my playlist!</Button>
    </>
  );
};

export default Questionnaire;