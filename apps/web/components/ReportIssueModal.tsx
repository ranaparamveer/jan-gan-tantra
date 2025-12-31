'use client'

import { useState } from 'react'

export default function ReportIssueModal({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
    const [loading, setLoading] = useState(false)
    // Helper for location - Moved up to fix Hook Rule
    const [userLocation, setUserLocation] = useState<{ lat: number, lng: number } | null>(null)

    const handleLocate = () => {
        navigator.geolocation.getCurrentPosition(
            (pos) => setUserLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
            (err) => alert("Could not access location. Please enable GPS.")
        )
    }

    if (!isOpen) return null

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        try {
            // New: Real API submission
            // We need: title, category_id (or slug?), location (point), description
            // For MVP: we'll hardcode a category if user didn't select, or map string to ID. 
            // Better: fetch categories. For now, let's assume valid data or just send minimal.

            // NOTE: Ideally we fetch categories from /api/wiki/categories/ to populate the dropdown
            // For this iteration, I'll send a default category ID = 1 (assuming it exists from seed) 
            // or just rely on backend default if allowed.

            const payload = {
                title: (e.target as any).title.value, // accessing form elements by name/id
                description: (e.target as any).description.value,
                category_id: 1, // Start with a default, TODO: Fetch real categories
                location: userLocation ? {
                    type: "Point",
                    coordinates: [userLocation.lng, userLocation.lat]
                } : null
            }

            if (!payload.location) {
                alert("Please enable location to report an issue.")
                setLoading(false)
                return
            }

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/issues/issues/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            })

            if (!res.ok) throw new Error("Failed to report issue")

            alert('Report submitted successfully! It will appear on the map shortly.')
            onClose()
            // Force refresh map? Window reload is crude but effective for MVP
            window.location.reload()

        } catch (err) {
            console.error(err)
            alert('Error submitting report. Please try again.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-black/50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full overflow-hidden">
                <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                    <h2 className="text-xl font-bold text-gray-900">Report an Issue</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600">✕</button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Issue Title</label>
                        <input name="title" type="text" required placeholder="e.g. Garbage pile on Main St" className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-200 outline-none" />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                        <select name="category" className="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none">
                            <option value="1">Sanitation</option>
                            <option value="2">Roads</option>
                            <option value="3">Water</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                        <button type="button" onClick={handleLocate} className={`w-full px-4 py-2 border border-dashed text-gray-500 hover:bg-gray-50 flex items-center justify-center gap-2 rounded-lg ${userLocation ? 'border-green-500 bg-green-50 text-green-700' : 'border-gray-300'}`}>
                            {userLocation ? '📍 Location Set' : '📍 Use My Current Location'}
                        </button>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                        <textarea name="description" className="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none h-24" placeholder="Describe the problem..."></textarea>
                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary-600 text-white py-3 rounded-lg font-bold hover:bg-primary-700 transition disabled:opacity-50"
                    >
                        {loading ? 'Submitting...' : 'Submit Report'}
                    </button>
                </form>
            </div>
        </div>
    )
}
