'use client'

import { useState } from 'react'
import EditSolutionModal from './EditSolutionModal'

export default function SolutionActions({ id, upvotes = 0 }: { id: string, upvotes?: number }) {
    const [votes, setVotes] = useState(upvotes)
    const [hasVoted, setHasVoted] = useState(false)
    const [isEditOpen, setIsEditOpen] = useState(false)

    const handleVote = async (type: 'up' | 'down') => {
        if (hasVoted) return

        try {
            // Optimistic update
            setVotes(prev => type === 'up' ? prev + 1 : prev - 1)
            setHasVoted(true)

            if (type === 'up') {
                await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/wiki/solutions/${id}/upvote/`, {
                    method: 'POST',
                })
            }
        } catch (err) {
            // Revert if failed
            setVotes(prev => type === 'up' ? prev - 1 : prev + 1)
            setHasVoted(false)
            alert('Failed to register vote')
        }
    }

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'Jan-Gan-Tantra Solution',
                    url: window.location.href
                })
            } catch (err) {
                // Share cancelled
            }
        } else {
            try {
                await navigator.clipboard.writeText(window.location.href)
                alert('Link copied to clipboard!')
            } catch (err) {
                alert('Could not copy link')
            }
        }
    }

    const handleDownvote = async () => {
        // Optimistic update
        setVotes(prev => Math.max(0, prev - 1))

        try {
            await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/wiki/solutions/${id}/downvote/`, {
                method: 'POST'
            })
        } catch (err) {
            console.error(err)
            // Rollback
            setVotes(prev => prev + 1)
        }
    }

    return (
        <>
            <div className="flex items-center gap-3">
                <div className="flex items-center bg-gray-100 rounded-lg p-1">
                    <button
                        onClick={() => handleVote('up')}
                        disabled={hasVoted}
                        className={`p-2 rounded hover:bg-white hover:shadow-sm transition ${hasVoted ? 'opacity-50' : ''}`}
                        title="Helpful"
                    >
                        👍
                    </button>
                    <span className="px-2 font-bold text-gray-700">{votes}</span>
                    <button
                        onClick={() => handleVote('down')}
                        disabled={hasVoted}
                        className={`p-2 rounded hover:bg-white hover:shadow-sm transition ${hasVoted ? 'opacity-50' : ''}`}
                        title="Not Helpful"
                    >
                        👎
                    </button>
                </div>

                <button
                    onClick={() => setIsEditOpen(true)}
                    className="p-2 text-gray-500 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition"
                    title="Suggest Edits"
                >
                    ✏️ Edit
                </button>

                <button
                    onClick={handleShare}
                    className="p-2 text-gray-500 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition"
                    title="Share"
                >
                    📤 Share
                </button>
            </div>

            {/* Edit Modal */}
            <EditSolutionModal
                isOpen={isEditModalOpen}
                onClose={() => setIsEditModalOpen(false)}
                solutionId={Number(id)}
            />
        </>
    )
}
