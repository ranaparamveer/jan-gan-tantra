import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'Jan-Gan-Tantra | People\'s System',
    description: 'Empowering citizens to navigate bureaucracy and solve civic problems',
    keywords: ['civic tech', 'india', 'government', 'accountability', 'RTI'],
    manifest: '/manifest.json',
}

export const viewport = {
    themeColor: '#0ea5e9',
    width: 'device-width',
    initialScale: 1,
    maximumScale: 5,
}

import Header from '@/components/Header'

import { LocationProvider } from '@/context/LocationContext'

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <LocationProvider>
                    <Header />
                    {children}
                </LocationProvider>
            </body>
        </html>
    )
}
