'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

// Reusing types roughly
interface Item {
    id: number
    title: string
    subtitle: string
    link: string
    type: 'issue' | 'solution'
}

import { useLocation } from '@/context/LocationContext'

// ... (imports)

export default function NearbyStats() {
    const [stats, setStats] = useState<{ issues: Item[], solutions: Item[] }>({ issues: [], solutions: [] })
    const [loading, setLoading] = useState(false)
    const { location } = useLocation()

    // Removed local geolocation logic - replaced by context

    useEffect(() => {
        if (!location) {
            setLoading(false)
            return
        }
        setLoading(true)

        const fetchData = async () => {
            // ... (rest of fetch logic remains same)
        }

        fetchData()
    }, [location])

    if (!location) return (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
            <p className="text-gray-600 mb-2">Search your location above to see local stats</p>
        </div>
    )

    // ...


    return (
        <div className="space-y-6">
            {/* Top 5 Issues */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-5 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                    <h3 className="font-bold text-gray-900">🚨 Top Local Issues</h3>
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full">Near You</span>
                </div>
                <div className="divide-y divide-gray-100">
                    {loading ? <div className="p-4 text-sm text-gray-500">Loading...</div> : stats.issues.length === 0 ? <div className="p-4 text-sm text-gray-500">No major issues reported nearby.</div> :
                        stats.issues.map(item => (
                            <Link key={item.id} href={item.link} className="block p-4 hover:bg-gray-50 transition">
                                <p className="font-medium text-gray-900 line-clamp-1">{item.title}</p>
                                <p className="text-xs text-gray-500 mt-1">{item.subtitle}</p>
                            </Link>
                        ))
                    }
                </div>
            </div>

            {/* Top 5 Solutions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-5 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                    <h3 className="font-bold text-gray-900">💡 Popular Solutions</h3>
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Trending</span>
                </div>
                <div className="divide-y divide-gray-100">
                    {loading ? <div className="p-4 text-sm text-gray-500">Loading...</div> : stats.solutions.length === 0 ? <div className="p-4 text-sm text-gray-500">No solutions found.</div> :
                        stats.solutions.map(item => (
                            <Link key={item.id} href={item.link} className="block p-4 hover:bg-gray-50 transition">
                                <p className="font-medium text-gray-900 line-clamp-1">{item.title}</p>
                                <p className="text-xs text-green-600 font-semibold mt-1">{item.subtitle}</p>
                            </Link>
                        ))
                    }
                </div>
            </div>
        </div>
    )
}
