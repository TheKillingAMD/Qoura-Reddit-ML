import NextAuth from "next-auth";
import Providers from 'next-auth/providers';
import axios from 'axios';

const providers = [
    Providers.Credentials({
        name: 'Credentials',
        authorize: async credentials => {
            const user = await axios.post('http://localhost:5000/login',
                {
                    email: credentials.email,
                    password: credentials.password
                });
            return user.data;
        }
    })
];

const callbacks = {
    async jwt(token, user) {
        if (user) {
            token.accessToken = user.accessToken;
            token.email = user.email;
        }

        return token;
    },

    async session(session, token) {
        session.accessToken = token.accessToken;
        session.user = token.email;
        return session;
    }
};

const options = {
    providers,
    callbacks,
    
};

export default (req, res) => NextAuth(req, res, options);