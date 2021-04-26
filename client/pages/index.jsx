import axios from '../utils/axios';
import { Container } from 'react-bootstrap';
import { useSession } from 'next-auth/client';
import useSWR from 'swr';

import Navbar from '../components/Navbar';
import QBox from '../components/QBox';

const fetcher = url => axios.get(url).then(res => res.data);

export default function Home(props) {
    const [session] = useSession();
    const { data, error } = useSWR('/papi', fetcher, { initialData: props.questions });
    const { questions } = data;
    // console.log(session);
    // console.log(session?.avatarURL);
    if (error)
        return (
            <>
                <Navbar session={session} />
                <Container fluid className='px-5 mb-5'>
                    <h1 className='text-center'>FAILED TO LOAD!</h1>
                </Container>
            </>
        );
    if (!questions)
        return (
            <>
                <Navbar session={session} />
                <Container fluid className='px-5 mb-5'>
                    <h1 className='text-center'>LOADING...</h1>
                </Container>
            </>
        );
    return (
        <>
            <Navbar session={session} />
            <Container fluid id='questions' className='px-5 mb-5'>
                {questions.map((q, i) => {
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

export async function getStaticProps() {
    const { questions } = await fetcher('/papi');
    return {
        props: { questions },
    };
}
