import axios from 'axios';
import { Container } from 'react-bootstrap';

import Navbar from '../../components/Navbar';

export default function Question({ data }) {
    return (
        <>
            <Navbar />
            <Container fluid className='px-5'>
                {data.map((v, i) => (
                    <div key={i}>
                        <p>{v['Answer']}</p>
                        <p>{v['User']}</p>
                    </div>
                ))}
            </Container>
        </>
    );
}

export async function getServerSideProps({ params }) {
    const id = params.id;
    const { Answers: data } = await axios
        .get('http://127.0.0.1:5000/question/' + id)
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
