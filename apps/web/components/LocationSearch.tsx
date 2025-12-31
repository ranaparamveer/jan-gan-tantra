'use client'

import { useState, useEffect, useRef } from 'react'
import { useLocation } from '@/context/LocationContext'

interface SearchResult {
    lat: string
    lon: string
    display_name: string
}

export default function LocationSearch() {
    const { location, setLocation, useCurrentLocation } = useLocation()
    const [query, setQuery] = useState('')
    const [results, setResults] = useState<SearchResult[]>([])
    const [isOpen, setIsOpen] = useState(false)
    const containerRef = useRef<HTMLDivElement>(null)

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(async () => {
            if (query.length < 3) {
                setResults([])
                return
            }

            try {
                const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
                const data = await res.json()
                setResults(data)
                setIsOpen(true)
            } catch (err) {
                console.error(err)
            }
        }, 500)

        return () => clearTimeout(timer)
    }, [query])

    // Sync input with global location
    useEffect(() => {
        if (location?.label) {
            setQuery(location.label)
        }
    }, [location])

    // Close dropdown on click outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const handleSelect = (result: SearchResult) => {
        setLocation({
            lat: parseFloat(result.lat),
            lng: parseFloat(result.lon),
            label: result.display_name.split(',')[0],
        })
        setQuery(result.display_name.split(',')[0])
        setIsOpen(false)
    }

    return (
        <div className="relative w-full max-w-md" ref={containerRef}>
            <div className="flex relative">
                <span className="absolute left-3 top-2.5 text-gray-400">📍</span>
                <input
                    type="text"
                    value={query}
                    onChange={(e) => {
                        setQuery(e.target.value)
                        setIsOpen(true)
                    }}
                    placeholder="Search city or area..."
                    className="w-full pl-10 pr-20 py-2 border border-gray-300 rounded-full focus:ring-2 focus:ring-primary-100 outline-none text-sm text-gray-900"
                />
                <button
                    type="button"
                    onClick={() => {
                        useCurrentLocation()
                        setIsOpen(false)
                    }}
                    className="absolute right-1 top-1 bottom-1 px-3 bg-gray-100 hover:bg-gray-200 text-xs text-primary-700 font-medium rounded-full transition"
                    title="Use current location"
                >
                    GPS
                </button>
            </div>

            {/* Dropdown Results */}
            {isOpen && results.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-lg shadow-xl border border-gray-100 max-h-60 overflow-y-auto z-[1000]">
                    {results.map((result, idx) => (
                        <button
                            key={idx}
                            onClick={() => handleSelect(result)}
                            className="w-full text-left px-4 py-3 hover:bg-gray-50 text-sm text-gray-700 border-b border-gray-50 last:border-0"
                        >
                            {result.display_name}
                        </button>
                    ))}
                </div>
            )}
        </div>
    )
}
