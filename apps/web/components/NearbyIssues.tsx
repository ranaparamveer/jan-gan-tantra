'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

interface Issue {
    id: number
    title: string
    status_display: string
    distance?: number
}

interface Feature {
    id: number
    properties?: {
        title: string
        status_display: string
    }
    title?: string
    status_display?: string
}

export default function NearbyIssues() {
    const [issues, setIssues] = useState<Issue[]>([])
    const [loading, setLoading] = useState(true)
    const [location, setLocation] = useState<{ lat: number, lng: number } | null>(null)

    useEffect(() => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLocation({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    })
                },
                (err) => {
                    console.error("Loc error", err)
                    setLoading(false)
                }
            )
        } else {
            setLoading(false)
        }
    }, [])

    useEffect(() => {
        if (!location) return

        const fetchIssues = async () => {
            try {
                // Fetch issues within 5km radius
                const res = await fetch(
                    `${process.env.NEXT_PUBLIC_API_URL}/api/issues/issues/?lat=${location.lat}&lng=${location.lng}&radius=5`
                )
                if (res.ok) {
                    const data = await res.json()
                    // Handle GeoJSON response (results.features or features)
                    const features = data.results?.features || data.features || []
                    setIssues(features.slice(0, 5).map((f: Feature) => ({
                        id: f.id,
                        title: f.properties?.title || f.title,
                        status_display: f.properties?.status_display || f.status_display,
                        distance: 0 // Placeholder
                    })))
                }
            } catch (e) {
                console.error(e)
            } finally {
                setLoading(false)
            }
        }

        fetchIssues()
    }, [location])

    if (loading) return <div className="text-gray-500 text-sm">Locating nearby issues...</div>

    if (!location) return (
        <div className="bg-orange-50 p-4 rounded-lg border border-orange-100">
            <p className="text-sm text-orange-800">Please enable location access to see issues near you.</p>
        </div>
    )

    if (issues.length === 0) return null

    return (
        <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="font-bold text-gray-900 mb-4">Issues in your area</h3>
            <div className="space-y-3">
                {issues.map(issue => (
                    <div key={issue.id} className="flex justify-between items-center pb-2 border-b border-gray-50 last:border-0">
                        <div>
                            <p className="text-sm font-medium text-gray-900 line-clamp-1">{issue.title}</p>
                            <span className="text-xs text-gray-500">{issue.status_display}</span>
                        </div>
                        <Link href="/#map" className="text-xs text-primary-600 font-semibold hover:underline">
                            View
                        </Link>
                    </div>
                ))}
            </div>
            <Link href="/#map" className="block text-center mt-3 text-sm text-primary-600 hover:text-primary-700">
                View all on map →
            </Link>
        </div>
    )
}
