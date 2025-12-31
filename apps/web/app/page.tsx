'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import SearchBox from '@/components/SearchBox'
import ReportIssueModal from '@/components/ReportIssueModal'
import NearbyStats from '@/components/NearbyStats'

// Dynamic import for HeatMap to avoid SSR issues with Leaflet
const HeatMap = dynamic(() => import('@/components/HeatMap'), { ssr: false })

export default function Home() {
    const [_searchQuery, setSearchQuery] = useState('')
    const [language] = useState('en')
    const [isReportModalOpen, setIsReportModalOpen] = useState(false)

    const handleSearch = (query: string) => {
        setSearchQuery(query)
    }

    return (
        <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white" dir={language === 'hi' ? 'ltr' : 'ltr'}> { /* Simple direction handling */}

            {/* Hero Section with Search */}
            <section className="py-12 px-4">
                <div className="max-w-7xl mx-auto text-center">
                    <h2 className="text-4xl font-bold text-gray-900 mb-4">
                        How can we help you today?
                    </h2>
                    <p className="text-lg text-gray-600 mb-8">
                        Search for solutions, report issues, or find the right government officer
                    </p>

                    <SearchBox onSearch={handleSearch} language={language} />

                    <div className="mt-6 flex flex-wrap justify-center gap-3">
                        <button
                            onClick={() => setSearchQuery('garbage collection')}
                            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition"
                        >
                            🗑️ Garbage Collection
                        </button>
                        <button
                            onClick={() => setSearchQuery('pothole repair')}
                            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition"
                        >
                            🚧 Pothole Repair
                        </button>
                        <button
                            onClick={() => setSearchQuery('water supply')}
                            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition"
                        >
                            💧 Water Supply
                        </button>
                        <button
                            onClick={() => setSearchQuery('street lights')}
                            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm text-gray-700 transition"
                        >
                            💡 Street Lights
                        </button>
                    </div>
                </div>
            </section>

            {/* Two Column Layout */}
            <section className="max-w-7xl mx-auto px-4 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-1 gap-8">
                    {/* Map and Nearby Stats Column (Full Width) */}
                    <div id="map-and-stats">
                        <div className="mb-4 text-center">
                            <h3 className="text-2xl font-bold text-gray-900">Issues Near You</h3>
                            <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                                Real-time civic issues reported by citizens
                            </p>
                        </div>

                        <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
                            {/* Left Sidebar: Stats & Top Lists (Wider now for side-by-side) */}
                            <div className="lg:col-span-2">
                                <NearbyStats />
                            </div>

                            {/* Right: Map Area (Narrower) */}
                            <div className="lg:col-span-1 relative">
                                <div className="h-[500px] rounded-xl overflow-hidden shadow-md border border-gray-200 relative bg-gray-100">
                                    <HeatMap />

                                    {/* Floating Report Button on Map */}
                                    <button
                                        onClick={() => setIsReportModalOpen(true)}
                                        className="absolute bottom-6 right-6 bg-primary-600 text-white px-6 py-3 rounded-full shadow-lg hover:bg-primary-700 transition z-[400] flex items-center gap-2 font-semibold"
                                    >
                                        📢 Report Issue
                                    </button>
                                </div>
                                <p className="text-xs text-gray-500 mt-2 text-right">Map shows reported issues in your region.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <ReportIssueModal isOpen={isReportModalOpen} onClose={() => setIsReportModalOpen(false)} />

            {/* Stats Section */}
            <section className="bg-primary-50 py-12 mt-12">
                <div className="max-w-7xl mx-auto px-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
                        <div>
                            <p className="text-4xl font-bold text-primary-700">500+</p>
                            <p className="text-gray-600 mt-2">Solutions Available</p>
                        </div>
                        <div>
                            <p className="text-4xl font-bold text-primary-700">22</p>
                            <p className="text-gray-600 mt-2">Indian Languages</p>
                        </div>
                        <div>
                            <p className="text-4xl font-bold text-primary-700">100%</p>
                            <p className="text-gray-600 mt-2">Free & Open Source</p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-gray-900 text-white py-8 mt-12">
                <div className="max-w-7xl mx-auto px-4 text-center">
                    <p className="text-sm">
                        Built for the people, by the people. Licensed under AGPL-3.0
                    </p>
                    <p className="text-xs text-gray-400 mt-2">
                        Empowering citizens to navigate bureaucracy and solve civic problems collectively.
                    </p>
                </div>
            </footer>
        </main>
    )
}
