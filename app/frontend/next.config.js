/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'standalone',
    async rewrites() {
        return [
            {
                source: '/api/:path*',
                destination: 'http://localhost:8001/api/:path*' // Proxy to Backend
            }
        ]
    }
}

module.exports = nextConfig
