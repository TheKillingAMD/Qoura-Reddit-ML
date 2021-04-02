import Head from 'next/head';
import styles from '../styles/Home.module.scss';
import axios from 'axios';

export default function Home({ data }) {
    return (
        <div className={styles.container}>
            <Head>
                <title>Create Next App</title>
                <link rel='icon' href='/favicon.ico' />
            </Head>

            <main className={styles.main}>
                <h1 className={styles.title}>
                    Welcome to <a href='https://nextjs.org'>Next.js!</a>
                </h1>
                {data.map(q => {
                    return (
                        <>
                            <p>{q['Question_Id']}</p>
                            <p>{q['Question']}</p>
                            <p>{q['User']}</p>
                            <p>{q['Answer']}</p>
                        </>
                    );
                })}

                <p className={styles.description}>
                    Get started by editing <code className={styles.code}>pages/index.js</code>
                </p>

                <div className={styles.grid}>
                    <a href='https://nextjs.org/docs' className={styles.card}>
                        <h3>Documentation &rarr;</h3>
                        <p>Find in-depth information about Next.js features and API.</p>
                    </a>

                    <a href='https://nextjs.org/learn' className={styles.card}>
                        <h3>Learn &rarr;</h3>
                        <p>Learn about Next.js in an interactive course with quizzes!</p>
                    </a>

                    <a
                        href='https://github.com/vercel/next.js/tree/master/examples'
                        className={styles.card}
                    >
                        <h3>Examples &rarr;</h3>
                        <p>Discover and deploy boilerplate example Next.js projects.</p>
                    </a>

                    <a
                        href='https://vercel.com/new?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app'
                        className={styles.card}
                    >
                        <h3>Deploy &rarr;</h3>
                        <p>Instantly deploy your Next.js site to a public URL with Vercel.</p>
                    </a>
                </div>
            </main>

            <footer className={styles.footer}>
                <a
                    href='https://vercel.com?utm_source=create-next-app&utm_medium=default-template&utm_campaign=create-next-app'
                    target='_blank'
                    rel='noopener noreferrer'
                >
                    Powered by <img src='/vercel.svg' alt='Vercel Logo' className={styles.logo} />
                </a>
            </footer>
        </div>
    );
}

export async function getServerSideProps() {
    const { questions: data } = await axios
        .get('http://127.0.0.1:5000')
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
