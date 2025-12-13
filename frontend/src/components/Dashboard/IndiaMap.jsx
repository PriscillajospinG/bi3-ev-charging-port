import React, { useEffect, useState } from 'react'
import { api } from '../../services/api'

const IndiaMap = () => {
    const [stations, setStations] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchStations = async () => {
            try {
                setLoading(true)
                // Default to India
                const response = await api.getStations({ country_code: 'IN', limit: 50 })
                setStations(response.data)
                setLoading(false)
            } catch (err) {
                console.error("Failed to fetch stations:", err)
                setError("Failed to load charging stations.")
                setLoading(false)
            }
        }

        fetchStations()
    }, [])

    return (
        <div className="bg-gray-800 rounded-lg p-6 shadow-lg border border-gray-700">
            <h2 className="text-xl font-bold text-white mb-4">India Charging Stations (Open Charge Map)</h2>

            {loading && <p className="text-gray-400">Loading stations...</p>}
            {error && <p className="text-red-400">{error}</p>}

            {!loading && !error && (
                <div className="overflow-x-auto">
                    <table className="min-w-full text-left text-sm text-gray-300">
                        <thead className="bg-gray-700 text-xs uppercase font-medium text-gray-400">
                            <tr>
                                <th className="px-4 py-3">Station Name</th>
                                <th className="px-4 py-3">Town/City</th>
                                <th className="px-4 py-3">State</th>
                                <th className="px-4 py-3">Usage</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-700">
                            {stations.map((station, index) => (
                                <tr key={station.ID || index} className="hover:bg-gray-700/50">
                                    <td className="px-4 py-3 font-medium text-white">
                                        {station.AddressInfo?.Title || 'Unknown'}
                                    </td>
                                    <td className="px-4 py-3">
                                        {station.AddressInfo?.Town || '-'}
                                    </td>
                                    <td className="px-4 py-3">
                                        {station.AddressInfo?.StateOrProvince || '-'}
                                    </td>
                                    <td className="px-4 py-3">
                                        {station.UsageType?.Title || 'Public'}
                                    </td>
                                </tr>
                            ))}
                            {stations.length === 0 && (
                                <tr>
                                    <td colSpan="4" className="px-4 py-6 text-center text-gray-500">
                                        No stations found.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    )
}

export default IndiaMap
