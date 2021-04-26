import axios from 'axios';

export default axios.create({
    baseURL: process.env.NODE_ENV === "production" ? "https://qr-ml.vercel.app" : "http://localhost:3000"
});