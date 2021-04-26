import axios from 'axios';
import { useState } from 'react';
import { Button, Container, Form } from 'react-bootstrap';
import { useSession } from 'next-auth/client';

import Navbar from '../components/Navbar';

export default function Home() {
    const [session] = useSession();
    const [values, setValues] = useState({ question: '' });
    const [adding, setAdding] = useState(false);

    if (session) {
        console.log('AT:', session);
    }

    const changeForm = e => {
        setValues({ ...values, [e.target.id]: e.target.value });
    };

    const submitForm = async e => {
        e.preventDefault();
        console.log(values);
        setAdding(true);
        const headers = {
            headers: {
                Authorization: `Bearer ${session.accessToken}`,
            },
        };
        console.log(values, headers);
        await axios
            .post('http://localhost:5000/add_question', values, headers)
            .then(response => {
                console.log(response.data);
                const { result } = response.data;
                if (result === 'Created successfully') {
                    console.log(response.data);
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
            <Navbar session={session} />
            {session ? (
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
            ) : (
                <h1 className='text-center'>YOU ARE NOT AUTHORIZED! BEGONE</h1>
            )}
        </>
    );
}
