import axios from 'axios';
import { useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';

import Navbar from '../components/Navbar';

export default function Home() {
    const [values, setValues] = useState({ email: '', password: '', username: '' });
    const [register, setRegister] = useState(false);

    const changeForm = e => {
        setValues({ ...values, [e.target.id]: e.target.value });
    };

    const submitForm = async e => {
        e.preventDefault();
        console.log(values);
        setRegister(true);
        await axios
            .post('http://localhost:5000/register', values)
            .then(response => {
                console.log(response.data);
                const { result } = response.data;
                if (result === 'Created successfully') {
                }
                setRegister(false);
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
                    <Form.Group controlId='username'>
                        <Form.Label>Username</Form.Label>
                        <Form.Control
                            type='text'
                            placeholder='Enter username'
                            onChange={changeForm}
                        />
                    </Form.Group>
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
                        {register ? <span>REGISTERING</span> : 'Submit'}
                    </Button>
                </Form>
            </Container>
        </>
    );
}
