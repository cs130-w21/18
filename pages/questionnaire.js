import React, { useEffect, useState } from "react";
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Button, Form } from 'react-bootstrap';

const Questionnaire = (props) => {
  const [responses, setResponses] = useState({
      energy: 5
  });

  const router = useRouter();

  const submitResponses = () => {
    console.log(responses);
    // make API call to submit responses

    router.push('/playlist/2');
  };

  return (
    <>
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
      <Button onClick={submitResponses}>Get my playlist!</Button>
    </>
  );
};

export default Questionnaire;
