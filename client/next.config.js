module.exports = {
    async rewrites() {
        return [
            {
                source: '/papi/:slug*',
                destination: process.env.NODE_ENV === "production" ? 'https://qr-ml-api.herokuapp.com/:slug*' : "http://localhost:5000/:slug*"
            },
        ]
    },
}