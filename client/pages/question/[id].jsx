import axios from 'axios';
import { Container } from 'react-bootstrap';

import Navbar from '../../components/Navbar';

export default function Question({ data }) {
    return (
        <>
            <Navbar />
            <Container fluid className='px-5'>
                {data}
            </Container>
        </>
    );
}

export async function getServerSideProps() {
    const data = 1
    return {
        props: { data },
    };
}
