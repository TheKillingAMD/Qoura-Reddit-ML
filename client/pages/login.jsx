import axios from 'axios';
import { useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';

import Navbar from '../components/Navbar';

export default function Home() {
    const [values, setValues] = useState({ email: '', password: '' });
    const [loggingIn, setLoggingIn] = useState(false);

    const changeForm = e => {
        setValues({ ...values, [e.target.id]: e.target.value });
    };

    const submitForm = async e => {
        e.preventDefault();
        console.log(values);
        setLoggingIn(true);
        await axios
            .post('http://localhost:5000/login', values)
            .then(response => {
                console.log(response.data);
                const {result} = response.data
                if(result === 'Login Successfully') {
                    
                }
                setLoggingIn(false);
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
                    <Form.Group controlId='email'>
                        <Form.Label>Email address</Form.Label>
                        <Form.Control
                            type='email'
                            placeholder='Enter email'
                            onChange={changeForm}
                        />
                    </Form.Group>
                    <Form.Group controlId='password'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type='password'
                            placeholder='Password'
                            onChange={changeForm}
                        />
                    </Form.Group>
                    <Button variant='primary' type='submit'>
                        {loggingIn ? <span>LOGGING IN</span> : 'Submit'}
                    </Button>
                </Form>
            </Container>
        </>
    );
}
