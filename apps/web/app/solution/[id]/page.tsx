'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import axios from 'axios'

interface Solution {
    id: number
    title: string
    description: string
    category_name: string
    success_rate: number
    upvotes: number
    created_at: string
}

export default function SolutionDetailPage() {
    const { id } = useParams()
    const router = useRouter()
    const [solution, setSolution] = useState<Solution | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (!id) return

        const fetchSolution = async () => {
            try {
                // Fetching from Wiki Solutions API
                const { data } = await axios.get(`/api/wiki/solutions/${id}/`)
                setSolution(data)
            } catch (error) {
                console.error("Failed to fetch solution:", error)
            } finally {
                setLoading(false)
            }
        }

        fetchSolution()
    }, [id])

    const handleVote = async (type: 'upvote' | 'downvote') => {
        if (!solution) return
        try {
            const { data } = await axios.post(`/api/wiki/solutions/${id}/${type}/`)
            setSolution(prev => prev ? { ...prev, upvotes: data.upvotes } : null)
        } catch (error) {
            console.error("Failed to vote:", error)
            alert("Failed to submit vote. Please try again.")
        }
    }

    if (loading) return <div className="p-8 text-center">Loading solution details...</div>
    if (!solution) return <div className="p-8 text-center text-red-500">Solution not found.</div>

    return (
        <div className="container mx-auto px-4 py-8 max-w-3xl">
            <button
                onClick={() => router.back()}
                className="mb-6 text-gray-500 hover:text-gray-900 flex items-center gap-1"
            >
                ← Back
            </button>

            <div className="bg-white rounded-xl shadow-lg border border-green-100 overflow-hidden">
                <div className="bg-green-50 px-8 py-4 border-b border-green-100 flex justify-between items-center">
                    <div className="flex items-center gap-2">
                        <span className="text-xl">✅</span>
                        <span className="font-semibold text-green-800">Verified Solution</span>
                    </div>
                </div>

                <div className="p-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">{solution.title}</h1>
                    <p className="text-sm text-gray-500 mb-6 font-medium">{solution.category_name}</p>

                    <div className="prose max-w-none text-gray-700 mb-8 leading-relaxed">
                        {solution.description}
                    </div>

                    <div className="flex items-center justify-between border-t border-gray-100 pt-6">
                        <div className="flex gap-4">
                            <button
                                onClick={() => handleVote('upvote')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-50 hover:bg-green-100 transition border border-green-200"
                            >
                                <span>👍</span>
                                <span className="font-semibold text-green-800">{solution.upvotes}</span>
                                <span className="text-xs text-green-700">Helpful</span>
                            </button>

                            <button
                                onClick={() => handleVote('downvote')}
                                className="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-50 hover:bg-red-100 transition border border-red-200"
                            >
                                <span>👎</span>
                                <span className="text-xs text-red-700">Not Helpful</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
