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
    const isTyping = useRef(false)

    // Debounce search
    useEffect(() => {
        // Only search if user is actively typing
        if (!isTyping.current) return

        const timer = setTimeout(async () => {
            if (query.length < 3) {
                setResults([])
                return
            }

            try {
                // Fetch boundingbox for smart zoom
                const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5`)
                const data = await res.json()
                setResults(data)
                setIsOpen(true)
            } catch (err) {
                console.error(err)
            }
        }, 500)

        return () => clearTimeout(timer)
    }, [query])

    // Sync input with global location (from map movement)
    useEffect(() => {
        if (location?.label) {
            // Prevent dropdown from opening when map updates label
            isTyping.current = false
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

    const handleSelect = (result: any) => {
        isTyping.current = false

        let bbox: [number, number, number, number] | undefined = undefined
        if (result.boundingbox) {
            // Nominatim returns [minLat, maxLat, minLon, maxLon] as strings
            // We want [minLat, minLng, maxLat, maxLng]
            bbox = [
                parseFloat(result.boundingbox[0]),
                parseFloat(result.boundingbox[2]),
                parseFloat(result.boundingbox[1]),
                parseFloat(result.boundingbox[3])
            ]
        }

        setLocation({
            lat: parseFloat(result.lat),
            lng: parseFloat(result.lon),
            label: result.display_name.split(',')[0],
            bbox: bbox
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
                        isTyping.current = true
                        setQuery(e.target.value)
                        setIsOpen(true) // Ensure open on manual type
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
