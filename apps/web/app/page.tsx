'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import SearchBox from '@/components/SearchBox'
import SolutionList from '@/components/SolutionList'

// Dynamic import for HeatMap to avoid SSR issues with Leaflet
const HeatMap = dynamic(() => import('@/components/HeatMap'), { ssr: false })

export default function Home() {
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedIssue, setSelectedIssue] = useState<any>(null)

    const handleSearch = (query: string) => {
        setSearchQuery(query)
    }

    const handleIssueClick = (issue: any) => {
        setSelectedIssue(issue)
    }

    return (
        <main className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 sticky top-0 z-10 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-primary-700">Jan-Gan-Tantra</h1>
                            <p className="text-sm text-gray-600">जन-गण-तंत्र | People's System</p>
                        </div>
                        <nav className="flex gap-4 text-sm">
                            <a href="#solutions" className="text-gray-600 hover:text-primary-600">Solutions</a>
                            <a href="#map" className="text-gray-600 hover:text-primary-600">Issues Map</a>
                            <a href="/about" className="text-gray-600 hover:text-primary-600">About</a>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Hero Section with Search */}
            <section className="py-12 px-4">
                <div className="max-w-7xl mx-auto text-center">
                    <h2 className="text-4xl font-bold text-gray-900 mb-4">
                        How can we help you today?
                    </h2>
                    <p className="text-lg text-gray-600 mb-8">
                        Search for solutions, report issues, or find the right government officer
                    </p>

                    <SearchBox onSearch={handleSearch} language="en" />

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
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Solutions Column */}
                    <div id="solutions">
                        <div className="mb-4">
                            <h3 className="text-2xl font-bold text-gray-900">
                                {searchQuery ? `Solutions for "${searchQuery}"` : 'Popular Solutions'}
                            </h3>
                            <p className="text-sm text-gray-600 mt-1">
                                Step-by-step guides to solve civic problems
                            </p>
                        </div>
                        <SolutionList searchQuery={searchQuery} language="en" />
                    </div>

                    {/* Map Column */}
                    <div id="map">
                        <div className="mb-4">
                            <h3 className="text-2xl font-bold text-gray-900">Issues Near You</h3>
                            <p className="text-sm text-gray-600 mt-1">
                                Real-time civic issues reported by citizens
                            </p>
                        </div>
                        <div className="h-[600px] rounded-lg overflow-hidden border border-gray-200">
                            <HeatMap onIssueClick={handleIssueClick} />
                        </div>

                        {selectedIssue && (
                            <div className="mt-4 p-4 bg-white border border-gray-200 rounded-lg">
                                <h4 className="font-semibold text-gray-900">{selectedIssue.title}</h4>
                                <p className="text-sm text-gray-600 mt-1">{selectedIssue.category_name}</p>
                                <span className={`inline-block mt-2 px-3 py-1 rounded-full text-xs ${selectedIssue.status === 'resolved'
                                        ? 'bg-green-100 text-green-700'
                                        : 'bg-orange-100 text-orange-700'
                                    }`}>
                                    {selectedIssue.status_display}
                                </span>
                            </div>
                        )}
                    </div>
                </div>
            </section>

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
