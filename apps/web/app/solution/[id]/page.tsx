import NearbyIssues from '@/components/NearbyIssues'
import SolutionActions from '@/components/SolutionActions'

async function getSolution(id: string) {
    const apiUrl = process.env.INTERNAL_API_URL || process.env.NEXT_PUBLIC_API_URL
    const res = await fetch(`${apiUrl}/api/wiki/solutions/${id}/`, {
        cache: 'no-store'
    })

    if (!res.ok) {
        throw new Error('Failed to fetch solution')
    }

    return res.json()
}

export default async function SolutionPage({ params }: { params: { id: string } }) {
    const solution = await getSolution(params.id)

    return (
        <main className="min-h-screen bg-gray-50 py-12">
            <div className="max-w-3xl mx-auto px-4">
                <a href="/" className="text-sm text-gray-500 hover:text-gray-900 mb-6 inline-block">
                    ← Back to Home
                </a>

                <article className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                    <div className="p-8">
                        {/* Header */}
                        <div className="flex justify-between items-start mb-6">
                            <div>
                                <span className="inline-block px-3 py-1 bg-primary-50 text-primary-700 text-xs font-semibold rounded-full mb-3">
                                    {solution.category_name}
                                </span>
                                <h1 className="text-3xl font-bold text-gray-900 mb-4">{solution.title}</h1>
                                <SolutionActions id={params.id} upvotes={solution.upvotes || 0} />
                            </div>
                            <div className="text-right">
                                <span className="block text-2xl font-bold text-green-600">
                                    {Math.round(solution.success_rate * 100)}%
                                </span>
                                <span className="text-xs text-gray-500">Success Rate</span>
                            </div>
                        </div>

                        {/* Steps */}
                        <div className="mb-8">
                            <h2 className="text-xl font-semibold text-gray-900 mb-4">Action Plan</h2>
                            <div className="space-y-4">
                                {solution.steps.map((step: string, index: number) => (
                                    <div key={index} className="flex gap-4 p-4 bg-gray-50 rounded-lg border border-gray-100">
                                        <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-primary-600 text-white rounded-full font-bold">
                                            {index + 1}
                                        </div>
                                        <p className="text-gray-700 pt-1">{step}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex flex-col sm:flex-row gap-4 pt-6 border-t border-gray-100">
                            <button className="flex-1 px-6 py-3 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-semibold transition text-center">
                                Start This Process
                            </button>
                            <button className="flex-1 px-6 py-3 border border-gray-300 hover:bg-gray-50 text-gray-700 rounded-lg font-semibold transition text-center">
                                Download PDF Guide
                            </button>
                        </div>
                    </div>
                </article>

                {/* Related Info */}
                <div className="mt-8 grid md:grid-cols-2 gap-6">
                    <NearbyIssues />

                    <div className="p-6 bg-white rounded-lg border border-gray-200">
                        <h3 className="font-bold text-gray-900 mb-2">Success Stories</h3>
                        <p className="text-sm text-gray-600 mb-4">
                            See how 24 other citizens successfully resolved this issue in your area.
                        </p>
                        <a href="#" className="text-primary-600 text-sm font-semibold hover:underline">
                            View Success Paths →
                        </a>
                    </div>
                </div>
            </div>
        </main>
    )
}
