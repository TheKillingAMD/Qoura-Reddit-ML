import { Navbar as ReactNavbar, Nav, Image } from 'react-bootstrap';
import { signOut } from 'next-auth/client';

import Avatar from '../Avatar';

import styles from './Navbar.module.scss';

export default function Navbar({ session }) {
    if (session) {
        console.log('AT:', session);
    }

    return (
        <ReactNavbar className={styles.navbar + ' justify-content-between'}>
            <ReactNavbar.Brand href='/'>QR-ML</ReactNavbar.Brand>
            <Nav>
                {/* <Avatar text={avatar} present={true} /> */}

                {session ? (
                    <>
                        <Nav.Link className={styles.nav_link} href='/addquestion'>
                            ADD QUESTION
                        </Nav.Link>
                        <Nav.Link className={styles.nav_link} onClick={() => signOut()}>
                            LOG OUT
                        </Nav.Link>
                        {session.avatarURL ===
                        'https://res.cloudinary.com/thekillingamd/image/upload/v1612692376/Profile%20Pictures/hide-facebook-profile-picture-notification_q15wp8.jpg' ? (
                            <Avatar text={session.user} />
                        ) : (
                            <Image
                                className='mx-2'
                                src={session.avatarURL}
                                roundedCircle
                                width='40px'
                                height='40px'
                            />
                        )}
                    </>
                ) : (
                    <>
                        <Nav.Link className={styles.nav_link} href='/register'>
                            SIGN UP
                        </Nav.Link>
                        <Nav.Link className={styles.nav_link} href='/login'>
                            LOG IN
                        </Nav.Link>
                    </>
                )}
            </Nav>
        </ReactNavbar>
    );
}
