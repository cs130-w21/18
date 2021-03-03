import React, { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import PageHead from "../components/head";
import styles from "../styles/Questionnaire.module.css";

const Questionnaire = (props) => {
  const [responses, setResponses] = useState(props.defaultSettings);

  const handleChange = (e) => {
    var min = parseFloat((parseFloat(e.target.value) - 0.2).toFixed(2));
    if (min < 0.0) {
      min = 0.0;
    }
    var max = parseFloat((parseFloat(e.target.value) + 0.2).toFixed(2));
    if (max > 1.0) {
      max = 1.0;
    }

    setResponses((prevResponses) => ({
      ...prevResponses,
      [e.target.id]: [min, max, parseFloat(e.target.value)],
    }));
  };

  return (
    <>
      <PageHead />
      {props.error !== "" ? (
        <Alert
          variant="primary"
          className="justify-content-md-center w-50 mx-auto mb-0"
        >
          {props.error}
        </Alert>
      ) : (
        ""
      )}
      <div className={styles.formContainer}>
        <Form>
          <div className={styles.title}>
            Tell us what kind of music you're in the mood for!
          </div>
          <Form.Group controlId="name">
            <div className={styles.moodNameContainer}>
              <Form.Label className={styles.formText}>
                Name your mood
              </Form.Label>
              <Form.Control
                className={styles.inputBox}
                type="text"
                onChange={(e) =>
                  setResponses((prevResponses) => ({
                    ...prevResponses,
                    name: e.target.value,
                  }))
                }
              />
            </div>
          </Form.Group>
          <Form.Group controlId="danceability">
            <Form.Label className={styles.formText}>Danceability</Form.Label>
            <Form.Control
              type="range"
              className={styles.slider}
              min="0.0"
              max="1.0"
              step="0.01"
              defaultValue="0.5"
              onChange={(e) => handleChange(e)}
            />
          </Form.Group>
          <Form.Group controlId="instrumentalness">
            <Form.Label className={styles.formText}>
              Instrumentalness
            </Form.Label>
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
            <Form.Label className={styles.formText}>Popularity</Form.Label>
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
            <Form.Label className={styles.formText}>Speechiness</Form.Label>
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
            <Form.Label className={styles.formText}>Valence</Form.Label>
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
            <Form.Label className={styles.formText}>Energy</Form.Label>
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
        <Button
          className={styles.getPlaylistBtn}
          onClick={() => props.submitResponses(responses)}
        >
          Get my playlist!
        </Button>
      </div>
    </>
  );
};

export default Questionnaire;
