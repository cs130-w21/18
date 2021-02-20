import React, { useState } from "react";
import { Button, Form } from "react-bootstrap";
import PageHead from "../components/head";

const Questionnaire = (props) => {
  const [responses, setResponses] = useState(props.defaultSettings);

  const handleChange = (e) => {
    setResponses((prevResponses) => ({ ...prevResponses, [e.target.id]: parseFloat(e.target.value) }));
  }
  
  return (
    <>
      <PageHead/>
      <div>
        <p>Tell us what kind of music you're in the mood for!</p>
      </div>
      <Form>
        <Form.Group controlId="danceability">
          <Form.Label>Danceability</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
        <Form.Group controlId="instrumentalness">
          <Form.Label>Instrumentalness</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
        <Form.Group controlId="popularity">
          <Form.Label>Popularity</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
        <Form.Group controlId="speechiness">
          <Form.Label>Speechiness</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
        <Form.Group controlId="valence">
          <Form.Label>Valence</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
        <Form.Group controlId="energy">
          <Form.Label>Energy</Form.Label>
          <Form.Control
            type="range"
            className="form-range"
            min="0.0"
            max="1.0"
            step="0.01"
            defaultValue="0.5"
            onChange={(e) => handleChange(e)}
          />
        </Form.Group>
      </Form>
      <Button onClick={() => props.submitResponses(responses)}>Get my playlist!</Button>
    </>
  );
};

export default Questionnaire;