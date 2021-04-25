import { Navbar as ReactNavbar, Nav, Image } from 'react-bootstrap';
import { signOut } from 'next-auth/client';

import Avatar from '../Avatar';

import styles from './Navbar.module.scss';

export default function Navbar({ avatar }) {
    return (
        <ReactNavbar className={styles.navbar + ' justify-content-between'}>
            <ReactNavbar.Brand href='/'>QR-ML</ReactNavbar.Brand>
            <Nav>
                {/* <Avatar text={avatar} present={true} /> */}
                {avatar && <Image src={avatar} roundedCircle width="40px" height="40px" />}
                <Nav.Link className={styles.nav_link} href='/addquestion'>
                    ADD QUESTION
                </Nav.Link>
                <Nav.Link className={styles.nav_link} href='/login'>
                    LOG IN
                </Nav.Link>
                <Nav.Link className={styles.nav_link} onClick={() => signOut()}>
                    LOG OUT
                </Nav.Link>
                <Nav.Link className={styles.nav_link} href='/register'>
                    SIGN UP
                </Nav.Link>
            </Nav>
        </ReactNavbar>
    );
}
