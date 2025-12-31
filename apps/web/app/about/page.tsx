export default function AboutPage() {
    return (
        <main className="min-h-screen bg-white">
            <div className="max-w-4xl mx-auto px-4 py-12">
                <h1 className="text-4xl font-bold text-gray-900 mb-6">About Jan-Gan-Tantra</h1>

                <div className="prose prose-lg text-gray-700">
                    <p className="lead text-xl">
                        Jan-Gan-Tantra (People's System) is an open-source civic technology platform designed to empower citizens
                        to navigate bureaucracy and solve public issues collectively.
                    </p>

                    <h2 className="text-2xl font-semibold mt-8 mb-4">Our Mission</h2>
                    <p>
                        We believe that technology can bridge the gap between citizens and the state. By making government
                        processes transparent and accountability visible, we aim to:
                    </p>
                    <ul className="list-disc pl-6 space-y-2 mt-4">
                        <li>Demystify complex bureaucratic procedures through simplified "How-To" guides.</li>
                        <li> visualize the performance of public infrastructure through real-time heatmaps.</li>
                        <li>Connect citizens with the right officers responsible for their area.</li>
                        <li>Facilitate collective action through clustered reporting and auto-generated petitions.</li>
                    </ul>

                    <h2 className="text-2xl font-semibold mt-8 mb-4">How it Works</h2>
                    <div className="grid md:grid-cols-2 gap-6 mt-4">
                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h3 className="font-bold text-lg mb-2">1. Search Solution</h3>
                            <p>Use our AI-powered search (voice or text) to find the exact procedure for your problem.</p>
                        </div>
                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h3 className="font-bold text-lg mb-2">2. Report Issues</h3>
                            <p>Geo-tag infrastructure failures. We verify and cluster them to alert authorities.</p>
                        </div>
                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h3 className="font-bold text-lg mb-2">3. Track Progress</h3>
                            <p>See your issue on the public dashboard and get updates as the government responds.</p>
                        </div>
                        <div className="bg-gray-50 p-6 rounded-lg">
                            <h3 className="font-bold text-lg mb-2">4. Escalate</h3>
                            <p>If unresolved, use our auto-generated grievance letters to escalate to higher-ups.</p>
                        </div>
                    </div>

                    <h2 className="text-2xl font-semibold mt-8 mb-4">Open Source</h2>
                    <p>
                        This project is built by volunteers. The code is available on <a href="#" className="text-primary-600 hover:underline">GitHub</a>.
                        We welcome contributors from all backgrounds—developers, designers, policy experts, and citizens.
                    </p>
                </div>
            </div>
        </main>
    )
}
