import axios from 'axios';
import { Container, Table, Image } from 'react-bootstrap';
import { useSession } from 'next-auth/client';

import Navbar from '../../components/Navbar';
import Avatar from '../../components/Avatar';

export default function Question({ data }) {
    const [session] = useSession();
    console.log(session);
    console.log(session?.avatarURL);

    return (
        <>
            <Navbar session={session} />
            <Container className='px-5'>
                <h2>{data['Question'][0]}</h2>
                <h5 className='mb-5 text-muted'>Asked By: {data['Question'][1]}</h5>
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
