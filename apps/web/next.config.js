/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    trailingSlash: true,
    images: {
        domains: ['localhost'],
    },
    async rewrites() {
        const API_URL = process.env.API_URL || 'http://127.0.0.1:8000'
        return [
            {
                source: '/api/:path*/',
                destination: `${API_URL}/api/:path*/`,
            },
            {
                source: '/api/:path*',
                destination: `${API_URL}/api/:path*/`, // Ensure trailing slash is passed to Django
            },
        ]
    },
}

module.exports = nextConfig
