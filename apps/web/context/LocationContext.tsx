'use client'

import React, { createContext, useContext, useState, useEffect } from 'react'

interface Location {
    lat: number
    lng: number
    label: string
}

interface LocationContextType {
    location: Location | null
    setLocation: (loc: Location | null) => void
    loading: boolean
    useCurrentLocation: () => void
}

const LocationContext = createContext<LocationContextType | undefined>(undefined)

export function LocationProvider({ children }: { children: React.ReactNode }) {
    const [location, setLocation] = useState<Location | null>(null)
    const [loading, setLoading] = useState(false)

    // Initial load from storage or default
    useEffect(() => {
        const stored = localStorage.getItem('user_location')
        if (stored) {
            try {
                setLocation(JSON.parse(stored))
            } catch (e) {
                console.error("Failed to parse stored location", e)
            }
        }
    }, [])

    const handleSetLocation = (loc: Location | null) => {
        setLocation(loc)
        if (loc) {
            localStorage.setItem('user_location', JSON.stringify(loc))
        } else {
            localStorage.removeItem('user_location')
        }
    }

    const useCurrentLocation = () => {
        setLoading(true)
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords
                    // Optional: Reverse geocode to get label
                    const newLocation = { lat: latitude, lng: longitude, label: 'Current Location' }
                    handleSetLocation(newLocation)
                    setLoading(false)
                },
                (error) => {
                    console.error("Location error", error)
                    setLoading(false)
                    alert("Could not get your location. Please check browser permissions.")
                }
            )
        } else {
            setLoading(false)
            alert("Geolocation is not supported by your browser.")
        }
    }

    return (
        <LocationContext.Provider value={{ location, setLocation: handleSetLocation, loading, useCurrentLocation }}>
            {children}
        </LocationContext.Provider>
    )
}

export function useLocation() {
    const context = useContext(LocationContext)
    if (context === undefined) {
        throw new Error('useLocation must be used within a LocationProvider')
    }
    return context
}
