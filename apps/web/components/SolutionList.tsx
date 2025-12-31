'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface Solution {
    id: number
    title: string
    description: string
    category_name: string
    language: string
    success_rate: number
    is_verified: boolean
    created_at: string
}

interface SolutionListProps {
    category?: string
    language?: string
    searchQuery?: string
}

export default function SolutionList({ category, language = 'en', searchQuery }: SolutionListProps) {
    const [solutions, setSolutions] = useState<Solution[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)

    useEffect(() => {
        const fetchSolutions = async () => {
            setLoading(true)
            setError(null)

            try {
                const params = new URLSearchParams()
                if (category) params.append('category', category)
                if (language) params.append('language', language)
                if (searchQuery) params.append('search', searchQuery)

                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_API_URL}/api/wiki/solutions/?${params.toString()}`
                )

                if (!response.ok) {
                    throw new Error('Failed to fetch solutions')
                }

                const data = await response.json()
                setSolutions(data.results || [])
            } catch (err) {
                setError(err instanceof Error ? err.message : 'An error occurred')
            } finally {
                setLoading(false)
            }
        }

        fetchSolutions()
    }, [category, language, searchQuery])

    if (loading) {
        return (
            <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        )
    }

    if (error) {
        return (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-600">Error: {error}</p>
            </div>
        )
    }

    if (solutions.length === 0) {
        return (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 text-center">
                <p className="text-gray-600">No solutions found. Try a different search or category.</p>
            </div>
        )
    }

    return (
        <div className="space-y-4">
            {solutions.map((solution) => (
                <Link
                    key={solution.id}
                    href={`/solutions/${solution.id}`}
                    className="block bg-white border border-gray-200 rounded-lg p-6 hover:shadow-lg 
                     hover:border-primary-300 transition-all duration-200"
                >
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                                <h3 className="text-lg font-semibold text-gray-900">
                                    {solution.title}
                                </h3>
                                {solution.is_verified && (
                                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                                        ✓ Verified
                                    </span>
                                )}
                            </div>

                            <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                                {solution.description}
                            </p>

                            <div className="flex items-center gap-4 text-sm text-gray-500">
                                <span className="px-3 py-1 bg-gray-100 rounded-full">
                                    {solution.category_name}
                                </span>
                                <span>
                                    ✅ {solution.success_rate.toFixed(0)}% success rate
                                </span>
                                <span>
                                    {new Date(solution.created_at).toLocaleDateString()}
                                </span>
                            </div>
                        </div>

                        <div className="ml-4">
                            <div className="flex flex-col items-center justify-center w-16 h-16 bg-primary-50 rounded-lg">
                                <span className="text-2xl font-bold text-primary-600">
                                    {solution.success_rate.toFixed(0)}
                                </span>
                                <span className="text-xs text-primary-600">%</span>
                            </div>
                        </div>
                    </div>
                </Link>
            ))}
        </div>
    )
}
