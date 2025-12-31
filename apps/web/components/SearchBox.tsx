'use client'

import { useState, useRef } from 'react'
import { MicrophoneIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline'

interface SearchBoxProps {
    onSearch: (query: string) => void
    placeholder?: string
    language?: string
}

export default function SearchBox({ onSearch, placeholder = "What is your problem?", language = 'en' }: SearchBoxProps) {
    const [query, setQuery] = useState('')
    const [isRecording, setIsRecording] = useState(false)
    const [isTranscribing, setIsTranscribing] = useState(false)
    const mediaRecorderRef = useRef<MediaRecorder | null>(null)
    const audioChunksRef = useRef<Blob[]>([])

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault()
        if (query.trim()) {
            onSearch(query)
        }
    }

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
            const mediaRecorder = new MediaRecorder(stream)
            mediaRecorderRef.current = mediaRecorder
            audioChunksRef.current = []

            mediaRecorder.ondataavailable = (event) => {
                audioChunksRef.current.push(event.data)
            }

            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
                await transcribeAudio(audioBlob)
                stream.getTracks().forEach(track => track.stop())
            }

            mediaRecorder.start()
            setIsRecording(true)
        } catch (error) {
            console.error('Error accessing microphone:', error)
            alert('Could not access microphone. Please check permissions.')
        }
    }

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop()
            setIsRecording(false)
        }
    }

    const transcribeAudio = async (audioBlob: Blob) => {
        setIsTranscribing(true)

        try {
            const formData = new FormData()
            formData.append('audio_file', audioBlob, 'recording.wav')
            formData.append('language', language)

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/voice-to-text/`, {
                method: 'POST',
                body: formData,
            })

            if (!response.ok) {
                throw new Error('Transcription failed')
            }

            const data = await response.json()
            setQuery(data.transcribed_text)
            onSearch(data.transcribed_text)
        } catch (error) {
            console.error('Transcription error:', error)
            alert('Failed to transcribe audio. Please try typing instead.')
        } finally {
            setIsTranscribing(false)
        }
    }

    return (
        <form onSubmit={handleSearch} className="w-full max-w-3xl mx-auto">
            <div className="relative flex items-center">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={placeholder}
                    className="w-full px-6 py-4 pr-32 text-lg border-2 border-gray-300 rounded-full 
                     focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200
                     transition-all duration-200"
                    disabled={isRecording || isTranscribing}
                />

                <div className="absolute right-2 flex items-center gap-2">
                    {/* Voice Input Button */}
                    <button
                        type="button"
                        onClick={isRecording ? stopRecording : startRecording}
                        disabled={isTranscribing}
                        className={`p-3 rounded-full transition-all duration-200 ${isRecording
                                ? 'bg-red-500 hover:bg-red-600 animate-pulse'
                                : isTranscribing
                                    ? 'bg-gray-400 cursor-not-allowed'
                                    : 'bg-primary-500 hover:bg-primary-600'
                            } text-white`}
                        title={isRecording ? 'Stop recording' : 'Voice search'}
                    >
                        <MicrophoneIcon className="w-5 h-5" />
                    </button>

                    {/* Search Button */}
                    <button
                        type="submit"
                        disabled={!query.trim() || isRecording || isTranscribing}
                        className="p-3 rounded-full bg-primary-600 hover:bg-primary-700 
                       disabled:bg-gray-300 disabled:cursor-not-allowed
                       text-white transition-all duration-200"
                        title="Search"
                    >
                        <MagnifyingGlassIcon className="w-5 h-5" />
                    </button>
                </div>
            </div>

            {/* Status Messages */}
            {isRecording && (
                <p className="mt-2 text-sm text-red-600 text-center animate-pulse">
                    🎤 Recording... Click the microphone again to stop
                </p>
            )}
            {isTranscribing && (
                <p className="mt-2 text-sm text-gray-600 text-center">
                    ⏳ Transcribing your voice...
                </p>
            )}
        </form>
    )
}
