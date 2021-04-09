import { Navbar as ReactNavbar, Nav } from 'react-bootstrap';

import styles from './Navbar.module.scss';
import { signOut } from 'next-auth/client';

export default function Navbar() {
    return (
        <ReactNavbar className={styles.navbar + ' justify-content-between'}>
            <ReactNavbar.Brand href='/'>QR-ML</ReactNavbar.Brand>
            <Nav>
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
