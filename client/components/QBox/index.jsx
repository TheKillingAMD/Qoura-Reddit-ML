import { Card } from 'react-bootstrap';

import styles from './QBox.module.scss';

export default function QBox({ question }) {
    return (
        <a href={'/question/' + question['Question_Id']} className='text-decoration-none'>
            <Card className={styles.card}>
                <Card.Body>
                    <Card.Title>{question['Question']}</Card.Title>
                    <Card.Subtitle className='text-muted'>{question['User']}</Card.Subtitle>
                </Card.Body>
            </Card>
        </a>
    );
}
