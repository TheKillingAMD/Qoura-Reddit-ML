import { Navbar as ReactNavbar, Nav } from 'react-bootstrap';

import styles from './Navbar.module.scss';

export default function Navbar() {
    return (
        <ReactNavbar className={styles.navbar + ' justify-content-between'}>
            <ReactNavbar.Brand href='/'>QR-ML</ReactNavbar.Brand>
            <Nav>
                <Nav.Link className={styles.nav_link} href='/login'>LOG IN</Nav.Link>
                <Nav.Link className={styles.nav_link} href='/register'>SIGN UP</Nav.Link>
            </Nav>
        </ReactNavbar>
    );
}
