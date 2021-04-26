import axios from 'axios';
import { Container, Table, Image, Button, Form } from 'react-bootstrap';
import { useState } from 'react';
import { useSession } from 'next-auth/client';
import { useRouter } from 'next/router';

import Navbar from '../../components/Navbar';
import Avatar from '../../components/Avatar';

export default function Question({ data }) {
    const [session] = useSession();
    const [answer, setAnswer] = useState({ answer: '' });
    const [isVisible, setIsVisible] = useState(false);
    const [adding, setAdding] = useState(false);

    const router = useRouter();
    const { id } = router.query;

    const changeAnswer = e => {
        setAnswer({ answer: e.target.value });
        console.log('ANS:', answer);
    };

    const toggleInput = _ => {
        setIsVisible(!isVisible);
    };

    const submitForm = async e => {
        e.preventDefault();
        setAdding(true);
        const headers = {
            headers: {
                Authorization: `Bearer ${session.accessToken}`,
            },
        };
        console.log(`${id} - ${answer} - ${headers}`);
        await axios
            .post('http://localhost:5000/add_answer/' + id, answer, headers)
            .then(response => {
                console.log(response.data);
                const { result } = response.data;
                if (result === 'Answer Added successfully') {
                    console.log(response.data);
                }
                setAdding(false);
            })
            .catch(error => {
                console.log(error);
            });
        window.location.reload();
        return 'SUCCESS';
    };

    // console.log(session);
    // console.log(session?.avatarURL);

    return (
        <>
            <Navbar session={session} />
            <Container className='px-5'>
                <h2>{data['Question'][0]}</h2>
                <h5 className='mb-3 text-muted'>Asked By: {data['Question'][1]}</h5>
                {session && (
                    <>
                        <Button
                            className='mb-3'
                            onClick={toggleInput}
                            style={{ display: !isVisible ? 'block' : 'none' }}
                        >
                            ADD ANSWER
                        </Button>
                        <div
                            className='answer-inp'
                            style={{ display: !isVisible ? 'none' : 'block' }}
                        >
                            <Form onSubmit={submitForm} method='POST'>
                                <Form.Group controlId='answer'>
                                    <Form.Control
                                        as='textarea'
                                        placeholder='Enter answer'
                                        rows={3}
                                        onChange={changeAnswer}
                                    />
                                    <Button
                                        className='mt-2 mr-2'
                                        variant='success'
                                        size='sm'
                                        type='submit'
                                    >
                                        {adding ? <span>SUBMITTING</span> : 'Submit'}
                                    </Button>
                                    <Button
                                        className='mt-2'
                                        variant='danger'
                                        size='sm'
                                        onClick={toggleInput}
                                    >
                                        Cancel
                                    </Button>
                                </Form.Group>
                            </Form>
                        </div>
                    </>
                )}
                <Table>
                    <tbody>
                        {data['Answer'].map((v, i) => (
                            <tr key={i} className='mb-3'>
                                <td>
                                    {v[1][1] ===
                                    'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg' ? (
                                        <Avatar text={v[1][0]} />
                                    ) : (
                                        <Image
                                            src={v[1][1]}
                                            roundedCircle
                                            width='40px'
                                            height='40px'
                                        />
                                    )}
                                </td>
                                <td className='align-middle'>
                                    <div>
                                        <h6 className='text-muted'>{v[1][0]}</h6>
                                        <p className='m-0'>{v[2]}</p>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            </Container>
        </>
    );
}

export async function getServerSideProps({ params }) {
    const id = params.id;
    const data = await axios
        .get('http://127.0.0.1:5000/question/' + id)
        .then(function (response) {
            let ans = response.data.Answer;
            console.log(ans.sort((a1, a2) => parseFloat(a2[0]) - parseFloat(a1[0])));
            // console.log(response.data.Answer);
            return response.data;
        })
        .catch(function (error) {
            console.log(error);
        });
    return {
        props: { data },
    };
}
