'use client'

import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix Leaflet default marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
})

interface Issue {
    id: number
    title: string
    category_name: string
    status: string
    location: {
        type: string
        coordinates: [number, number]
    }
    upvotes: number
}

interface HeatMapProps {
    center?: [number, number]
    zoom?: number
    onIssueClick?: (issue: Issue) => void
}

export default function HeatMap({
    center = [28.6139, 77.2090], // Default: New Delhi
    zoom = 12,
    onIssueClick
}: HeatMapProps) {
    const mapRef = useRef<L.Map | null>(null)
    const mapContainerRef = useRef<HTMLDivElement>(null)
    const [issues, setIssues] = useState<Issue[]>([])
    const [loading, setLoading] = useState(true)
    const markersRef = useRef<L.Marker[]>([])

    // Initialize map
    useEffect(() => {
        if (!mapContainerRef.current || mapRef.current) return

        const map = L.map(mapContainerRef.current).setView(center, zoom)

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19,
        }).addTo(map)

        mapRef.current = map

        return () => {
            map.remove()
            mapRef.current = null
        }
    }, [])

    // Fetch issues when map moves
    useEffect(() => {
        if (!mapRef.current) return

        const fetchIssues = async () => {
            setLoading(true)
            try {
                const bounds = mapRef.current!.getBounds()
                const bbox = [
                    bounds.getWest(),
                    bounds.getSouth(),
                    bounds.getEast(),
                    bounds.getNorth()
                ].join(',')

                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_URL}/api/issues/issues/?bbox=${bbox}&status=reported`
                )

                if (!response.ok) throw new Error('Failed to fetch issues')

                const data = await response.json()
                setIssues(data.features || [])
            } catch (error) {
                console.error('Error fetching issues:', error)
            } finally {
                setLoading(false)
            }
        }

        const map = mapRef.current
        map.on('moveend', fetchIssues)
        fetchIssues() // Initial load

        return () => {
            map.off('moveend', fetchIssues)
        }
    }, [])

    // Update markers when issues change
    useEffect(() => {
        if (!mapRef.current) return

        // Clear existing markers
        markersRef.current.forEach(marker => marker.remove())
        markersRef.current = []

        // Add new markers
        issues.forEach((issue: any) => {
            const coords = issue.geometry.coordinates
            const marker = L.marker([coords[1], coords[0]])
                .addTo(mapRef.current!)
                .bindPopup(`
          <div class="p-2">
            <h3 class="font-bold text-sm">${issue.properties.title}</h3>
            <p class="text-xs text-gray-600">${issue.properties.category_name}</p>
            <p class="text-xs mt-1">
              <span class="px-2 py-1 rounded text-white text-xs ${issue.properties.status === 'resolved'
                        ? 'bg-green-500'
                        : 'bg-orange-500'
                    }">
                ${issue.properties.status_display}
              </span>
            </p>
            <p class="text-xs mt-1">👍 ${issue.properties.upvotes} upvotes</p>
          </div>
        `)

            marker.on('click', () => {
                if (onIssueClick) {
                    onIssueClick(issue.properties)
                }
            })

            markersRef.current.push(marker)
        })
    }, [issues, onIssueClick])

    return (
        <div className="relative w-full h-full">
            <div ref={mapContainerRef} className="w-full h-full rounded-lg shadow-lg" />

            {loading && (
                <div className="absolute top-4 right-4 bg-white px-4 py-2 rounded-lg shadow-md">
                    <p className="text-sm text-gray-600">Loading issues...</p>
                </div>
            )}

            <div className="absolute bottom-4 left-4 bg-white px-4 py-3 rounded-lg shadow-md">
                <p className="text-sm font-semibold text-gray-700">
                    {issues.length} issues in this area
                </p>
            </div>
        </div>
    )
}
