'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import axios from 'axios'

interface Issue {
    id: number
    title: string
    description: string
    category_name: string
    status: string
    upvotes: number
    downvotes: number
    created_at: string
    location: {
        type: string
        coordinates: [number, number]
    }
}

export default function IssueDetailPage() {
    const { id } = useParams()
    const router = useRouter()
    const [issue, setIssue] = useState<Issue | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!id) return

        const fetchIssue = async () => {
            try {
                // Fetch issue details
                // Note: The API likely returns geometry as 'location' object.
                // Depending on serializer, it might be nested or flat.
                // Assuming standard DRF GeoJSON or custom serializer. 
                const { data } = await axios.get(`/api/issues/issues/${id}/`)
                setIssue(data)
            } catch (error) {
                console.error("Failed to fetch issue:", error)
            } finally {
                setLoading(false)
            }
        }

        fetchIssue()
    }, [id])

    const handleVote = async (type: 'upvote' | 'downvote') => {
        if (!issue) return
        try {
            const { data } = await axios.post(`/api/issues/issues/${id}/${type}/`)
            setIssue(prev => prev ? { ...prev, upvotes: data.upvotes, downvotes: data.downvotes || prev.downvotes } : null)
        } catch (error) {
            console.error("Failed to vote:", error)
            alert("Failed to submit vote. Please try again.")
        }
    }

    if (loading) return <div className="p-8 text-center">Loading issue details...</div>
    if (!issue) return <div className="p-8 text-center text-red-500">Issue not found.</div>

    return (
        <div className="container mx-auto px-4 py-8 max-w-3xl">
            <button
                onClick={() => router.back()}
                className="mb-6 text-gray-500 hover:text-gray-900 flex items-center gap-1"
            >
                ← Back
            </button>

            <div className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
                <div className="p-8">
                    <div className="flex justify-between items-start mb-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold tracking-wide uppercase 
                            ${issue.status === 'resolved' ? 'bg-green-100 text-green-700' : 'bg-orange-100 text-orange-700'}`}>
                            {issue.status.replace('_', ' ')}
                        </span>
                        <span className="text-gray-400 text-sm">
                            {new Date(issue.created_at).toLocaleDateString()}
                        </span>
                    </div>

                    <h1 className="text-3xl font-bold text-gray-900 mb-2">{issue.title}</h1>
                    <p className="text-sm text-gray-500 mb-6 font-medium">{issue.category_name}</p>

                    <div className="prose max-w-none text-gray-700 mb-8 leading-relaxed">
                        {issue.description}
                    </div>

                    <div className="flex items-center justify-between border-t border-gray-100 pt-6">
                        <div className="flex gap-4">
                            <button
                                onClick={() => handleVote('upvote')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-50 hover:bg-gray-100 transition border border-gray-200"
                            >
                                <span>⚠️</span>
                                <span className="font-semibold text-gray-700">{issue.upvotes}</span>
                                <span className="text-xs text-gray-500">I still have this issue</span>
                            </button>

                            <button
                                onClick={() => handleVote('downvote')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-50 hover:bg-gray-100 transition border border-gray-200"
                            >
                                <span>✅</span>
                                <span className="font-semibold text-gray-700">{issue.downvotes}</span>
                                <span className="text-xs text-gray-500">Fixed for me</span>
                            </button>
                        </div>

                        <div className="text-right">
                            {/* Placeholder for map or location name */}
                            <p className="text-xs text-gray-400">Location ID: {issue.id}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
