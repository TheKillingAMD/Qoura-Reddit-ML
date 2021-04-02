import { Card } from 'react-bootstrap';

import styles from './QBox.module.scss';

export default function QBox({ question }) {
    return (
        <Card className={styles.card}>
            <Card.Body>
                <Card.Title>{question['Question']}</Card.Title>
                <Card.Subtitle className='mb-3 text-muted'>{question['User']}</Card.Subtitle>
                <Card.Text>Add Question Description here</Card.Text>
                <Card.Text>
                    This will be used to route to Questions page - {question['Question_Id']}
                </Card.Text>
            </Card.Body>
        </Card>
    );
}
