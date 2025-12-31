'use client'

import { useState } from 'react'

export default function EditSolutionModal({ isOpen, onClose, solutionId }: { isOpen: boolean, onClose: () => void, solutionId: number }) {
    const [loading, setLoading] = useState(false)

    if (!isOpen) return null

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)

        try {
            // Need solution ID - component should accept it as prop.
            // Assuming this component is passed a solutionId prop which we will add now.

            const suggestion = (e.target as any).suggestion.value

            // NOTE: We need to pass solutionId prop to this modal. For now, failing if not present, but 
            // the parent component needs update. Assuming parent passes `solutionId` prop.

            const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/wiki/suggestions/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    solution: solutionId,
                    suggestion_text: suggestion
                })
            })

            if (!res.ok) throw new Error("Failed")

            alert('Suggestion received! Our moderators will review it.')
            onClose()
        } catch (e) {
            console.error(e)
            alert('Error sending suggestion')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed inset-0 z-[2000] flex items-center justify-center bg-black/50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-md w-full">
                <div className="p-6 border-b border-gray-100 flex justify-between items-center">
                    <h2 className="text-xl font-bold text-gray-900">Suggest an Edit</h2>
                    <button onClick={onClose} className="text-gray-400 hover:text-gray-600">✕</button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-4">
                    <p className="text-sm text-gray-600">Found an error or have a better way? Let us know.</p>
                    <textarea name="suggestion" className="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none h-32" placeholder="Your suggestion..."></textarea>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full bg-primary-600 text-white py-2 rounded-lg font-bold hover:bg-primary-700 transition disabled:opacity-50"
                    >
                        {loading ? 'Sending...' : 'Send Suggestion'}
                    </button>
                </form>
            </div>
        </div>
    )
}
