import axios from '../utils/axios';
import { Container } from 'react-bootstrap';
import { useSession } from 'next-auth/client';

import Navbar from '../components/Navbar';
import QBox from '../components/QBox';

export default function Home({ data }) {
    const [session] = useSession();
    // console.log(session);
    // console.log(session?.avatarURL);
    return (
        <>
            <Navbar session={session} />
            <Container fluid id='questions' className='px-5 mb-5'>
                {data.map((q, i) => {
                    return (
                        <div key={i} className='mb-4'>
                            <QBox question={q} />
                        </div>
                    );
                })}
            </Container>
        </>
    );
}

export async function getServerSideProps() {
    const { questions: data } = await axios
        .get('/papi')
        .then(function (response) {
            return response.data;
        })
        .catch(function (error) {
            console.log(error);
        });
    return {
        props: { data },
    };
}
