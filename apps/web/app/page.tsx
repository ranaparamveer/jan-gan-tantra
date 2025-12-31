export default function Home() {
    return (
        <main className="flex min-h-screen flex-col items-center justify-center p-8">
            <div className="max-w-4xl w-full text-center space-y-8">
                <h1 className="text-6xl font-bold text-primary-700">
                    Jan-Gan-Tantra
                </h1>
                <p className="text-2xl text-gray-600">
                    जन-गण-तंत्र | People's System
                </p>
                <p className="text-lg text-gray-500 max-w-2xl mx-auto">
                    Empowering citizens to navigate bureaucracy, hold authorities accountable,
                    and solve civic problems collectively.
                </p>

                <div className="mt-12 p-8 bg-white rounded-lg shadow-lg">
                    <h2 className="text-2xl font-semibold mb-4">Coming Soon</h2>
                    <ul className="text-left space-y-3 text-gray-700">
                        <li>✅ Project structure initialized</li>
                        <li>✅ Django backend with PostGIS</li>
                        <li>✅ Next.js frontend setup</li>
                        <li>⏳ Solution Wiki (Knowledge Layer)</li>
                        <li>⏳ Gov-Graph (Accountability Layer)</li>
                        <li>⏳ Pulse Dashboard (Visual Layer)</li>
                        <li>⏳ Multi-language AI support</li>
                    </ul>
                </div>
            </div>
        </main>
    )
}
