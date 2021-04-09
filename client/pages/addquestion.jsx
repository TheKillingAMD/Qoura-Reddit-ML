import axios from 'axios';
import { useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';

import Navbar from '../components/Navbar';

export default function Home() {
    const [values, setValues] = useState({ question: '' });
    const [adding, setAdding] = useState(false);

    const changeForm = e => {
        setValues({ ...values, [e.target.id]: e.target.value });
    };

    const submitForm = async e => {
        e.preventDefault();
        console.log(values);
        setAdding(true);
        await axios
            .post('http://localhost:5000/add_question', values)
            .then(response => {
                console.log(response.data);
                const { result, token } = response.data;
                console.log(token)
                if (result === 'Created successfully') {
                }
                setAdding(false);
            })
            .catch(error => {
                console.log(error);
            });
        return 'SUCCESS';
    };

    return (
        <>
            <Navbar />
            <Container fluid id='questions' className='px-5 mb-5'>
                <Form onSubmit={submitForm} method='POST'>
                    <Form.Group controlId='question'>
                        <Form.Label>Question</Form.Label>
                        <Form.Control
                            type='text'
                            placeholder='Enter question'
                            onChange={changeForm}
                        />
                    </Form.Group>
                    <Button variant='primary' type='submit'>
                        {adding ? <span>ADDING</span> : 'Submit'}
                    </Button>
                </Form>
            </Container>
        </>
    );
}
