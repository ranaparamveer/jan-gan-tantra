'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import axios from 'axios'
import { useLocation } from '@/context/LocationContext'

interface Item {
    id: number
    title: string
    category_name: string
    link: string
    type: 'issue' | 'solution'
    status: string
    upvotes: number
    downvotes: number
}

export default function NearbyStats() {
    const [stats, setStats] = useState<{ issues: Item[], solutions: Item[] }>({ issues: [], solutions: [] })
    const [loading, setLoading] = useState(false)
    const { location } = useLocation()

    // Helper to refresh data without full reload
    const fetchData = async () => {
        if (!location) return
        try {
            const params = {
                lat: location.lat,
                lng: location.lng,
                radius: 5,
            }

            // Parallel fetching
            const [issuesRes, solutionsRes] = await Promise.all([
                axios.get('/api/issues/issues/', { params }),
                axios.get('/api/wiki/solutions/', { params })
            ])

            // Process Issues
            const issueFeatures = issuesRes.data.results?.features || (Array.isArray(issuesRes.data.results) ? issuesRes.data.results : []) || []
            const topIssues = issueFeatures.map((f: any) => ({
                id: f.id,
                title: f.properties.title,
                category_name: f.properties.category_name,
                link: `/issues/${f.id}`,
                type: 'issue',
                status: f.properties.status, // e.g. 'reported', 'in_progress'
                upvotes: f.properties.upvotes || 0,
                downvotes: f.properties.downvotes || 0,
            }))
                .filter((i: any) => i.status !== 'resolved') // Ensure only active issues
                .sort((a: any, b: any) => b.upvotes - a.upvotes)
                .slice(0, 5)

            // Process Solutions
            // Solutions API returns standard array, not GeoJSON yet? Let's check viewset.
            // Viewset inherits ModelViewSet, but `Solution` has no GeoJSON serializer explicitly used for list?
            // Actually `SolutionListSerializer` is used. It's a ModelSerializer.
            // So response is `results: [...]` or just `[...]` depending on pagination.
            const solutionData = solutionsRes.data.results || (Array.isArray(solutionsRes.data) ? solutionsRes.data : []) || []
            const topSolutions = solutionData.map((s: any) => ({
                id: s.id,
                title: s.title,
                category_name: s.category_name,
                link: `/solution/${s.id}`, // Corrected URL
                type: 'solution',
                status: 'published',
                upvotes: s.upvotes || 0,
                downvotes: 0, // Backend downvote just decrements upvotes currently
            }))
                .sort((a: any, b: any) => b.upvotes - a.upvotes)
                .slice(0, 5)

            setStats({
                issues: topIssues,
                solutions: topSolutions
            })
        } catch (error) {
            console.error("Failed to fetch nearby stats:", error)
        }
    }

    useEffect(() => {
        if (!location) {
            setLoading(false)
            return
        }
        setLoading(true)
        fetchData().finally(() => setLoading(false))
    }, [location])

    const handleVote = async (e: React.MouseEvent, item: Item, type: 'upvote' | 'downvote') => {
        e.preventDefault() // Prevent link navigation
        try {
            const endpoint = item.type === 'solution'
                ? `/api/wiki/solutions/${item.id}/${type}/`
                : `/api/issues/issues/${item.id}/${type}/`

            await axios.post(endpoint)
            // Refresh data to show new counts
            fetchData()
        } catch (error) {
            console.error("Vote failed:", error)
        }
    }

    if (!location) return (
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 text-center">
            <p className="text-gray-600 mb-2">Search your location above to see local stats</p>
        </div>
    )

    return (
        <div className="space-y-6">
            {/* Top 5 Issues */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-5 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                    <h3 className="font-bold text-gray-900">🚨 Top Local Issues</h3>
                    <span className="text-xs bg-red-100 text-red-700 px-2 py-1 rounded-full">Active</span>
                </div>
                <div className="divide-y divide-gray-100">
                    {loading ? <div className="p-4 text-sm text-gray-500">Loading...</div> : stats.issues.length === 0 ? <div className="p-4 text-sm text-gray-500">No major issues reported nearby.</div> :
                        stats.issues.map(item => (
                            <div key={item.id} className="block p-4 hover:bg-gray-50 transition relative group">
                                <Link href={item.link} className="absolute inset-0 z-0" />
                                <div className="relative z-10 pointer-events-none">
                                    <p className="font-medium text-gray-900 line-clamp-1">{item.title}</p>
                                    <p className="text-xs text-gray-500 mt-1">{item.category_name} • {item.upvotes} reports • {item.downvotes} fixed</p>
                                </div>
                                <div className="relative z-20 mt-3 pointer-events-auto">
                                    <button
                                        onClick={(e) => handleVote(e, item, 'upvote')}
                                        className="text-xs bg-orange-100 hover:bg-orange-200 text-orange-800 px-3 py-1.5 rounded-full font-medium transition flex items-center gap-1 w-fit"
                                    >
                                        ⚠️ I still have this issue
                                    </button>
                                    <button
                                        onClick={(e) => handleVote(e, item, 'downvote')}
                                        className="text-xs bg-green-100 hover:bg-green-200 text-green-800 px-3 py-1.5 rounded-full font-medium transition flex items-center gap-1 ml-2"
                                    >
                                        ✅ Fixed for me
                                    </button>
                                </div>
                            </div>
                        ))
                    }
                </div>
            </div>

            {/* Top 5 Solutions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-5 py-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                    <h3 className="font-bold text-gray-900">💡 Top Local Solutions</h3>
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">Resolved</span>
                </div>
                <div className="divide-y divide-gray-100">
                    {loading ? <div className="p-4 text-sm text-gray-500">Loading...</div> : stats.solutions.length === 0 ? <div className="p-4 text-sm text-gray-500">No solutions found.</div> :
                        stats.solutions.map(item => (
                            <div key={item.id} className="block p-4 hover:bg-gray-50 transition relative">
                                <Link href={item.link} className="absolute inset-0 z-0" />
                                <div className="relative z-10 pointer-events-none">
                                    <p className="font-medium text-gray-900 line-clamp-1">{item.title}</p>
                                    <p className="text-xs text-green-600 font-semibold mt-1">
                                        {item.upvotes} useful
                                    </p>
                                </div>
                                <div className="relative z-20 mt-3 flex gap-2 pointer-events-auto">
                                    <button
                                        onClick={(e) => handleVote(e, item, 'upvote')}
                                        className="text-xs bg-green-100 hover:bg-green-200 text-green-800 px-3 py-1.5 rounded-full font-medium transition flex items-center gap-1"
                                    >
                                        👍 {item.upvotes}
                                    </button>
                                    <button
                                        onClick={(e) => handleVote(e, item, 'downvote')}
                                        className="text-xs bg-gray-100 hover:bg-gray-200 text-gray-600 px-3 py-1.5 rounded-full font-medium transition flex items-center gap-1"
                                    >
                                        👎
                                    </button>
                                </div>
                            </div>
                        ))
                    }
                </div>
            </div>
        </div>
    )
}
