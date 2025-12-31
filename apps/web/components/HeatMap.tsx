'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import { useLocation } from '@/context/LocationContext'
import axios from 'axios'

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
    properties?: any // Backend might send properties flatter or nested, adjusting for GeoJSON structure if needed
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
    const markersRef = useRef<L.Marker[]>([])
    const circlesRef = useRef<L.Circle[]>([])

    const { location, setLocation } = useLocation()

    // Fetch issues based on map bounds
    const fetchIssues = useCallback(async () => {
        if (!mapRef.current) return

        try {
            const bounds = mapRef.current.getBounds()
            // Format: min_lng,min_lat,max_lng,max_lat
            const bbox = bounds.toBBoxString()

            const { data } = await axios.get('/api/issues/issues/', {
                params: { bbox }
            })

            // Backend returns GeoJSON.
            // If paginated: { count: ..., results: { type: 'FeatureCollection', features: [...] } }
            // If not paginated: { type: 'FeatureCollection', features: [...] }
            let features = []
            if (data.type === 'FeatureCollection') {
                features = data.features || []
            } else if (data.results?.type === 'FeatureCollection') {
                features = data.results.features || []
            } else if (Array.isArray(data.results)) {
                features = data.results
            } else if (Array.isArray(data)) {
                features = data
            }

            const mappedIssues = features.map((f: any) => ({
                id: f.id,
                ...f.properties, // Spread title, category, status, upvotes
                location: f.geometry, // Map geometry to location
                properties: f.properties // Keep original properties just in case
            }))

            setIssues(mappedIssues)

        } catch (error) {
            console.error("Failed to fetch issues:", error)
        }
    }, [])

    // Initialize map
    useEffect(() => {
        if (!mapContainerRef.current || mapRef.current) return

        let isCancelled = false

        const initMap = async () => {
            // Load marker cluster dynamically
            try {
                if (!(L as any).markerClusterGroup) {
                    await import('leaflet.markercluster')
                }
            } catch (e) {
                console.warn("Failed to load markercluster", e)
            }

            if (isCancelled) return
            if (!mapContainerRef.current) return
            if (mapRef.current) return

            const map = L.map(mapContainerRef.current).setView(center, zoom)

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19,
            }).addTo(map)

            mapRef.current = map

            // Event Listeners
            map.on('moveend', () => {
                fetchIssues()

                // Sync to context
                const center = map.getCenter()
                setLocation({
                    lat: center.lat,
                    lng: center.lng,
                    label: 'Map Location'
                })
            })

            // Initial fetch
            fetchIssues()
        }

        initMap()

        // Cleanup
        return () => {
            isCancelled = true
            if (mapRef.current) {
                mapRef.current.remove()
                mapRef.current = null
            }
        }
    }, []) // Empty dependency array - run once on mount

    // Sync Global Location -> Map
    useEffect(() => {
        if (!mapRef.current || !location) return

        const currentCenter = mapRef.current.getCenter()
        const dist = Math.sqrt(
            Math.pow(currentCenter.lat - location.lat, 2) +
            Math.pow(currentCenter.lng - location.lng, 2)
        )

        // Only move if distance is significant (> ~50m) to prevent loops/jitters
        if (dist > 0.0005) {
            mapRef.current.setView([location.lat, location.lng], 14, { animate: true })
        }
    }, [location])

    // Render Markers & Clusters
    useEffect(() => {
        if (!mapRef.current) return

        // Cleanup existing
        markersRef.current.forEach(m => m.remove())
        circlesRef.current.forEach(c => c.remove())
        markersRef.current = []
        circlesRef.current = []

        if ((mapRef.current as any)._cluster) {
            mapRef.current.removeLayer((mapRef.current as any)._cluster)
        }

        // Init Cluster Group
        let markerClusterGroup: any = null
        if ((L as any).markerClusterGroup) {
            markerClusterGroup = (L as any).markerClusterGroup()
        }

        issues.forEach((issue) => {
            // Unpack location (GeoJSON Point: { type: 'Point', coordinates: [lng, lat] })
            // Note: GeoJSON is [lng, lat], Leaflet is [lat, lng]
            const [lng, lat] = issue.location.coordinates

            // 1. Heat Circle (Status-based color)
            const circleColor = issue.status === 'resolved' ? '#22c55e' : '#f97316'
            const heatCircle = L.circle([lat, lng], {
                color: circleColor,
                fillColor: circleColor,
                fillOpacity: 0.15,
                radius: 300, // Fixed radius for heat effect
                stroke: false
            }).addTo(mapRef.current!)
            circlesRef.current.push(heatCircle)

            // 2. Marker Interaction
            const marker = L.marker([lat, lng])
                .bindPopup(`
                    <div class="p-3 min-w-[200px]">
                        <h3 class="font-bold text-base mb-1">${issue.title}</h3>
                        <p class="text-xs text-gray-500 mb-2">${issue.category_name} • ${issue.status}</p>
                        <div class="flex items-center gap-2 mb-3">
                             <span class="px-2 py-1 rounded text-white text-xs ${issue.status === 'resolved' ? 'bg-green-500' : 'bg-orange-500'}">${issue.status}</span>
                             <span class="text-xs font-semibold">👍 ${issue.upvotes}</span>
                        </div>
                    </div>
                `)

            marker.on('click', () => {
                if (onIssueClick) onIssueClick(issue)
            })

            if (markerClusterGroup) {
                markerClusterGroup.addLayer(marker)
            } else {
                marker.addTo(mapRef.current!)
                markersRef.current.push(marker)
            }
        })

        if (markerClusterGroup) {
            mapRef.current.addLayer(markerClusterGroup)
                ; (mapRef.current as any)._cluster = markerClusterGroup
        }

    }, [issues, onIssueClick])

    const handleLocateMe = () => {
        if (!mapRef.current) return
        mapRef.current.locate({ setView: true, maxZoom: 14 })
    }

    return (
        <div className="relative w-full h-full z-0">
            <div ref={mapContainerRef} className="w-full h-full rounded-lg shadow-lg" />

            <button
                onClick={handleLocateMe}
                className="absolute top-20 right-4 md:top-4 md:right-4 bg-white w-10 h-10 flex items-center justify-center rounded-lg shadow-md z-[400] hover:bg-gray-50 border border-gray-200"
                title="Locate Me"
            >
                📍
            </button>

            <div className="absolute bottom-4 left-4 bg-white px-4 py-3 rounded-lg shadow-md z-[1000]">
                <p className="text-sm font-semibold text-gray-700">
                    {issues.length} issues in this area
                </p>
            </div>
        </div>
    )
}

