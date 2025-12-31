import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'Jan-Gan-Tantra | People\'s System',
    description: 'Empowering citizens to navigate bureaucracy and solve civic problems',
    keywords: ['civic tech', 'india', 'government', 'accountability', 'RTI'],
    manifest: '/manifest.json',
    themeColor: '#0ea5e9',
    viewport: 'width=device-width, initial-scale=1, maximum-scale=5',
}

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>{children}</body>
        </html>
    )
}
