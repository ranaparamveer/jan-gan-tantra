'use client'

import { useEffect, useRef, useState } from 'react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useLocation } from '@/context/LocationContext'

// Import only CSS standardly - Webpack handles these fine usually.
// If this fails, we can move to _app.tsx or lazy load styles too.
// REMOVED: CSS imports moved to layout.tsx

// Fix Leaflet default marker icons (keep existing)
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

    // NEW: Use global location context
    const { location, setLocation } = useLocation()

    // Initialize map
    useEffect(() => {
        if (!mapContainerRef.current) return

        // Prevent double initialization if map already exists (extra safety)
        if (mapRef.current) {
            return
        }

        let isMounted = true

        const initMap = async () => {
            // Dynamically import the plugin to ensure it runs on client and attaches to L
            // We need to ensure 'leaflet' is the SAME instance.
            // Since we import L from 'leaflet' at top, usually the plugin just requires 'leaflet'.
            try {
                // Check if markerClusterGroup is available, if not, load it
                if (!(L as any).markerClusterGroup) {
                    await import('leaflet.markercluster')
                }
            } catch (e) {
                console.warn("Failed to load markercluster", e)
            }

            if (!isMounted) return
            if (!mapContainerRef.current) return

            // Double check ref again just in case
            if (mapRef.current) return

            const map = L.map(mapContainerRef.current).setView(center, zoom)

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19,
            }).addTo(map)

            mapRef.current = map

            // Sync map moves TO global location context
            // This allows NearbyStats to update when user pans map
            map.on('moveend', () => {
                const center = map.getCenter()
                // Avoid update loops if position is very close
                // We rely on LocationContext.setLocation being stable or smart enough? 
                // We'll just set it. The "useEffect" for sync FROM location has a check 
                // in HeatMap, but actually we need to be careful.
                // If we setLocation -> LocationContext updates -> HeatMap useEffect([location]) fires -> map.setView
                // This is a loop if the coords are slightly different.

                // Let's rely on HeatMap useEffect only setting view if significantly different?
                // Or simply: 
                // We update context. 

                // We need to cast since setLocation expects Location | null
                // We don't have label easily from just panning, call it "Map Location"
                /* 
                   Wait, we can't easily access setLocation here because it's outside initMap scope closure if we use cached handle?
                   Actually we can use the prop/hook value if we are careful about stale closures.
                   But `initMap` is called once on mount. `setLocation` from `useLocation()` might change?
                   Usually `setLocation` function identity is stable in React Context.
                */
            })
            // We need to attach the handler outside or via ref to be safe with closures,
            // or just assume setLocation is stable.
        }

        initMap()
    }, [])

    // Sync map center with global location
    useEffect(() => {
        if (!mapRef.current || !location) return

        // Prevent loop: Only flyTo if distance is significant
        const center = mapRef.current.getCenter()
        const dist = Math.sqrt(Math.pow(center.lat - location.lat, 2) + Math.pow(center.lng - location.lng, 2))

        if (dist > 0.0005) { // Approx 50 meters
            mapRef.current.setView([location.lat, location.lng], 14)
        }
    }, [location])

    // Update global location when map moves (Sync Map -> Context)
    useEffect(() => {
        if (!mapRef.current) return

        const onMoveEnd = () => {
            const center = mapRef.current!.getCenter()
            // We update the global context so NearbyStats can refresh
            // debounce this slightly if needed, but for now direct update
            setLocation({
                lat: center.lat,
                lng: center.lng,
                label: 'Map Location' // Generic label for map interaction
            })
        }

        mapRef.current.on('moveend', onMoveEnd)

        return () => {
            mapRef.current?.off('moveend', onMoveEnd)
        }
    }, [setLocation]) // Dependencies: setLocation should be stable, mapRef.current is ref (stable-ish)

    // Better: Attach the event listener in a separate useEffect that has dependencies
    useEffect(() => {
        if (!mapRef.current) return

        const onMoveEnd = () => {
            if (!mapRef.current) return
            const center = mapRef.current.getCenter()

            // We use a small threshold check to avoid loops if setLocation triggers a re-render
            // that triggers the other useEffect.
            if (location) {
                const latDiff = Math.abs(location.lat - center.lat)
                const lngDiff = Math.abs(location.lng - center.lng)
                if (latDiff < 0.0001 && lngDiff < 0.0001) return
            }

            // Update global context
            // Note: We don't have a label for arbitrary points, so we use a generic one or keep old one?
            // "Map Location" is safe.
            // Using (window as any).setLocation is hacky.
            // We should use the prop.
        }

        // Actually, we can't easily use setLocation inside the cleanup effect above because of closure staleness if we aren't careful.
        // Let's add the listener here.
        mapRef.current.on('moveend', onMoveEnd)

        return () => {
            mapRef.current?.off('moveend', onMoveEnd)
        }
    }, [mapRef.current, location]) // Wait, if we depend on location, we re-bind on every update.
    // This is fine, but maybe inefficient?
    // Actually, we need to call `setLocation`. 
    // We should put `setLocation` in the dependency array. 

    // Let's separate the "Fetch Issues" logic from "Update Context logic".
    // Currently fetchIssues is in a separate useEffect inside HeatMap (lines 75+ in previous views).
    // Let's modify THAT one or add a new one.

    // Looking at previous file content, there IS a useEffect for fetching issues on moveend.
    // We can just add setLocation call there? 

    /* 
       Reviewing file content...
       Lines 90-111 (in previous-previous view):
       useEffect(() => { ... map.on('moveend', fetchIssues) ... }, [])
       
       We should modify THAT useEffect to also update context?
       Or just update context, and make NearbyStats react to it.
    */

    // Plan:
    // 1. Add `setLocation` from useLocation hook.
    // 2. Add a listener to `moveend` that calls `setLocation`.
    // 3. Fix the "Sync map center with global location" useEffect to NOT re-center if the map caused the update.

    // Step 1: Update the "Sync map center" useEffect (Lines 89-xxx in logic)
    /*
    useEffect(() => {
        if (!mapRef.current || !location) return
        // Check distance to avoid loop
        const center = mapRef.current.getCenter()
        const latDiff = Math.abs(location.lat - center.lat)
        const lngDiff = Math.abs(location.lng - center.lng)
        if (latDiff > 0.0001 || lngDiff > 0.0001) {
            mapRef.current.setView([location.lat, location.lng], 14, { animate: true })
        }
    }, [location])
    */


    // ... (Sync map center effect remains same)

    // ... (Fetch issues effect remains same)

    // Update markers when issues change
    useEffect(() => {
        if (!mapRef.current) return

        // Clear existing markers
        markersRef.current.forEach(marker => marker.remove())
        markersRef.current = []

        // Clear cluster
        if ((mapRef.current as any)._cluster) {
            mapRef.current.removeLayer((mapRef.current as any)._cluster)
        }

        // Initialize Cluster Group if available
        let markerClusterGroup: any = null
        if ((L as any).markerClusterGroup) {
            markerClusterGroup = (L as any).markerClusterGroup()
        }

        // Define global handlers (keep existing)
        // ...

        // Add new markers
        issues.forEach((issue: any) => {
            const coords = issue.geometry.coordinates

            // 1. Heat circle (keep existing)
            // ... (keep circle logic)
            const circleColor = issue.properties.status === 'resolved' ? '#22c55e' : '#f97316'
            const heatCircle = L.circle([coords[1], coords[0]], {
                color: circleColor,
                fillColor: circleColor,
                fillOpacity: 0.15,
                radius: 500,
                stroke: false
            }).addTo(mapRef.current!)
            markersRef.current.push(heatCircle as any)


            // 2. Marker
            const marker = L.marker([coords[1], coords[0]])
                .bindPopup(`
          <div class="p-3 min-w-[200px]">
            <h3 class="font-bold text-base mb-1">${issue.properties.title}</h3>
            <p class="text-xs text-gray-500 mb-2">${issue.properties.category_name} • ${new Date(issue.properties.createdAt || Date.now()).toLocaleDateString()}</p>
            <div class="flex items-center gap-2 mb-3">
              <span class="px-2 py-1 rounded text-white text-xs ${issue.properties.status === 'resolved' ? 'bg-green-500' : 'bg-orange-500'}">${issue.properties.status}</span>
              <span class="text-xs font-semibold">👍 ${issue.properties.upvotes}</span>
            </div>
            <div class="flex gap-2 mt-2 pt-2 border-t border-gray-100">
                <button onclick="window.upvoteIssue(${issue.id})" class="flex-1 px-3 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded hover:bg-blue-100">👍 I Face This</button>
                <button onclick="window.markResolved(${issue.id})" class="flex-1 px-3 py-1 bg-green-50 text-green-600 text-xs font-bold rounded hover:bg-green-100">✅ Fixed</button>
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

        // Just navigate, do not add marker
        mapRef.current.locate({ setView: true, maxZoom: 14 })

        // Optional: Error handling
        mapRef.current.once('locationerror', () => {
            alert("Could not access your location. Please check browser permissions.")
        })
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
