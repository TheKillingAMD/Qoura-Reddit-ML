import axios from 'axios';
import { useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';

import Navbar from '../components/Navbar';

export default function Home() {
    const [values, setValues] = useState({ email: '', password: '', username: '' });
    const [image, setImage] = useState();
    const [register, setRegister] = useState(false);

    const changeInputForm = e => {
        console.log(e.target.value);
        setValues({ ...values, [e.target.id]: e.target.value });
        console.log(values);
    };

    const changeImageForm = e => {
        console.log(e.target.files[0]);
        setImage(e.target.files[0]);
        console.log(image);
    };

    const submitForm = async e => {
        e.preventDefault();
        console.log(values);
        setRegister(true);
        const formData = new FormData();
        formData.append('image', image);
        // formData.append('data', values);
        Object.keys(values).forEach(key => {
            formData.append(key, values[key]);
        });
        await axios
            .post('http://localhost:5000/register', formData)
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
                            onChange={changeInputForm}
                        />
                    </Form.Group>
                    <Form.Group controlId='email'>
                        <Form.Label>Email address</Form.Label>
                        <Form.Control
                            type='email'
                            placeholder='Enter email'
                            onChange={changeInputForm}
                        />
                    </Form.Group>
                    <Form.Group controlId='password'>
                        <Form.Label>Password</Form.Label>
                        <Form.Control
                            type='password'
                            placeholder='Password'
                            onChange={changeInputForm}
                        />
                    </Form.Group>
                    <Form.Group>
                        <Form.File id='image' label='Upload Image' onChange={changeImageForm} />
                    </Form.Group>
                    <Button variant='primary' type='submit'>
                        {register ? <span>REGISTERING</span> : 'Submit'}
                    </Button>
                </Form>
            </Container>
        </>
    );
}
