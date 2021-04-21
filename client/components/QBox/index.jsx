import { Card } from 'react-bootstrap';

import styles from './QBox.module.scss';

export default function QBox({ question }) {
    return (
        <a href={'/question/' + question['Question_Id']} className='text-decoration-none'>
            <Card className={styles.card}>
                <Card.Body>
                    <Card.Title>{question['Question']}</Card.Title>
                    <Card.Subtitle className='mb-3 text-muted'>{question['User']}</Card.Subtitle>
                    <Card.Text>Add Question Description here</Card.Text>
                </Card.Body>
            </Card>
        </a>
    );
}
