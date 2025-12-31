'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

// import { useLocation } from '@/context/LocationContext'
import LocationSearch from './LocationSearch'

export default function Header() {
    const [language, setLanguage] = useState('en')
    const pathname = usePathname()
    // const { location, setLocation, useCurrentLocation } = useLocation()
    // const [locQuery, setLocQuery] = useState('')

    // Sync language across tabs/pages if needed (simple implementation)
    useEffect(() => {
        const stored = localStorage.getItem('language')
        if (stored) setLanguage(stored)
    }, [])

    // Sync local input with global location label
    // useEffect(() => {
    //     if (location?.label) setLocQuery(location.label)
    // }, [location])

    const handleLanguageChange = (lang: string) => {
        setLanguage(lang)
        localStorage.setItem('language', lang)
        // Dispatch event for other components to listen
        window.dispatchEvent(new CustomEvent('languageChange', { detail: lang }))
    }

    // handleLocationSearch removed - moved to LocationSearch component

    return (
        <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
            <div className="max-w-7xl mx-auto px-4 py-4">
                <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                    <div className="flex items-center justify-between w-full md:w-auto">
                        <Link href="/">
                            <div>
                                <h1 className="text-2xl font-bold text-primary-700">
                                    {language === 'en' ? 'Jan-Gan-Tantra' : 'जन-गण-तंत्र'}
                                </h1>
                                <p className="text-sm text-gray-600">
                                    {language === 'en' ? "People's System" : "जनता का सिस्टम"}
                                </p>
                            </div>
                        </Link>
                    </div>

                    {/* Location Search Bar */}
                    <div className="flex-1 max-w-md w-full mx-auto md:mx-4">
                        <LocationSearch />
                    </div>

                    <nav className="flex items-center gap-6 text-sm w-full md:w-auto justify-end">
                        <div className="hidden md:flex gap-4">
                            <Link href="/about" className="text-gray-600 hover:text-primary-600">About</Link>
                        </div>

                        <select
                            value={language}
                            onChange={(e) => handleLanguageChange(e.target.value)}
                            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block p-2.5"
                        >
                            <option value="en">English</option>
                            <option value="hi">हिंदी (Hindi)</option>
                        </select>
                    </nav>
                </div>
            </div>
        </header>
    )
}
