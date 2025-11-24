import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext.jsx'; 
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css'; 
import L from 'leaflet'; 

// Fix for default Leaflet marker icon not showing up in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
    iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});


// --- Configuration ---
const API_ALERTS_URL = 'http://127.0.0.1:8000/api/v1/alerts?count=50';
const REFRESH_INTERVAL_MS = 5000;
const DEFAULT_CENTER = [0.0, 37.0];
const DEFAULT_ZOOM = 5;
const ITEMS_PER_PAGE = 15; // Set pagination size as requested

// --- Custom Theme Colors ---
const COLORS = {
    BG_PRIMARY: '#131521',     // Deeper Dark Blue/Black
    UI_CARD: '#1c1f30',        // Slightly lighter slate for content cards
    ACCENT_LIGHT: '#F7E7CE',   // Cream/Beige (Main header/title color)
    ACCENT_CRITICAL: '#BA160C', // Deep Red/Maroon (Error/High Risk)
    ACCENT_WARNING: '#FFD700',  // Gold
    ACCENT_SUCCESS: '#2ECC40',  // Green
    TEXT_MUTED: '#9fa8da',     // Soft muted text
};

// --- Helper Components ---

const KPI_Card = ({ title, value, color, icon }) => (
    <div style={cardStyle}>
        <h5 style={kpiTitleStyle}>{title}</h5>
        <h2 style={{ ...kpiValueStyle, color: color }}>{value}</h2>
        <i className={`fa-solid fa-${icon}`} style={{ ...kpiIconStyle, color: color }}></i>
    </div>
);

const PaginationControls = ({ totalItems, itemsPerPage, currentPage, onPageChange }) => {
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    if (totalPages <= 1) return null;

    const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

    return (
        <div style={paginationContainerStyle}>
            {pages.map(page => (
                <button
                    key={page}
                    onClick={() => onPageChange(page)}
                    style={pageButtonStyle(page === currentPage)}
                >
                    {page}
                </button>
            ))}
        </div>
    );
};

const getRiskColor = (score) => {
    if (score > 0.8) return COLORS.ACCENT_CRITICAL;
    if (score > 0.6) return COLORS.ACCENT_WARNING;
    return COLORS.ACCENT_SUCCESS;
};


const Dashboard = () => {
    const { logout, token, user } = useAuth();
    const [rawData, setRawData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [apiError, setApiError] = useState(null);
    
    // --- Pagination State ---
    const [currentPage, setCurrentPage] = useState(1);
    
    // --- Filter State ---
    const [minRisk, setMinRisk] = useState(0.5);
    const [threatFilter, setThreatFilter] = useState('ALL');

    // Memoized filtering logic 
    const filteredAlerts = React.useMemo(() => {
        let filtered = rawData.filter(alert => alert.risk_score >= minRisk);

        if (threatFilter !== 'ALL') {
            if (threatFilter === 'Peaceful') {
                filtered = filtered.filter(alert => alert.peace_module_flag === true);
            } else {
                filtered = filtered.filter(alert => 
                    alert.threat_type && alert.threat_type.toLowerCase().includes(threatFilter.toLowerCase())
                );
            }
        }
        // Reset to first page whenever filters change
        setCurrentPage(1); 
        return filtered;
    }, [rawData, minRisk, threatFilter]);

    // Apply Pagination
    const paginatedAlerts = React.useMemo(() => {
        const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
        const endIndex = startIndex + ITEMS_PER_PAGE;
        return filteredAlerts.slice(startIndex, endIndex);
    }, [filteredAlerts, currentPage]);


    // --- Data Fetching Logic with Auto-Refresh ---

    const fetchAlerts = useCallback(async () => {
        if (!token) {
            setApiError("No authorization token found.");
            setLoading(false);
            return;
        }
        setLoading(true);

        try {
            const response = await axios.get(API_ALERTS_URL, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            setRawData(response.data); 
            setApiError(null);

        } catch (err) {
            console.error("API Fetch Error:", err);
            if (err.response && err.response.status === 401) {
                setApiError("Authentication failed. Please log in again.");
                logout(); 
            } else {
                setApiError("Failed to connect to FastAPI. Is the backend running?");
            }
        } finally {
            setLoading(false);
        }
    }, [token, logout]);

    // Setup periodic refresh
    useEffect(() => {
        fetchAlerts();
        const interval = setInterval(fetchAlerts, REFRESH_INTERVAL_MS);
        return () => clearInterval(interval); // Cleanup on component unmount
    }, [fetchAlerts]); 


    // --- KPI Calculations ---
    const totalAlerts = filteredAlerts.length;
    const maxRisk = totalAlerts > 0 ? Math.max(...filteredAlerts.map(a => a.risk_score)) : 0.0;
    const peaceActive = filteredAlerts.filter(a => a.peace_module_flag).length;
    const maxColor = getRiskColor(maxRisk);


    // --- Rendering ---

    if (apiError && !loading) {
        return (
            <div style={{ padding: '40px', color: COLORS.ACCENT_CRITICAL, backgroundColor: COLORS.BG_PRIMARY, minHeight: '100vh', fontFamily: 'system-ui, sans-serif' }}>
                <h2>Connection Error: Data Unavailable</h2>
                <p>{apiError}</p>
                <button onClick={logout} style={{backgroundColor: COLORS.ACCENT_CRITICAL, color: 'white', padding: '10px'}}>Log Out</button>
            </div>
        );
    }
    
    return (
        <div className="dashboard-container" style={dashboardContainerStyle}>
            {/* 1. HEADER (Title and Sign Out) */}
            <div style={headerStyle}>
                <h1 style={titleStyle}>🇰🇪 UlinziMind AI Sentinel: Real-Time Intelligence</h1>
                <button onClick={logout} style={signOutButtonStyle}>
                    Sign Out ({user ? user.email : 'User'})
                </button>
            </div>

            {/* 2. KPI Cards */}
            <div style={kpiRowStyle}>
                <KPI_Card title="Active Alerts (Filtered)" value={totalAlerts} color={COLORS.ACCENT_LIGHT} icon="bell" />
                <KPI_Card title="Max Risk Score" value={maxRisk.toFixed(2)} color={maxColor} icon="fire-extinguisher" />
                <KPI_Card title="Peace Protocols Active" value={peaceActive} color={COLORS.ACCENT_SUCCESS} icon="hand-holding-heart" />
            </div>

            {/* 3. MAIN CONTENT (Filters + Map) */}
            <div style={mainRowStyle}>
                {/* Left Sidebar for Filters/Controls */}
                <div style={sidebarStyle}>
                    <h4 style={sidebarTitleStyle}>Threat Filters</h4>
                    
                    <label style={labelStyle}>Minimum Risk Score: ({minRisk.toFixed(1)})</label>
                    <input
                        type="range"
                        min="0.0" max="1.0" step="0.1"
                        value={minRisk}
                        onChange={(e) => setMinRisk(parseFloat(e.target.value))}
                        style={rangeInputStyle}
                    />
                    
                    <label style={labelStyle}>Threat Type:</label>
                    <select
                        value={threatFilter}
                        onChange={(e) => setThreatFilter(e.target.value)}
                        style={dropdownStyle}
                    >
                        <option value="ALL">All Threats</option>
                        <option value="CRITICAL">CRITICAL: Coordinated Threat</option>
                        <option value="HIGH">HIGH: Escalating Unrest/Infiltration</option>
                        <option value="Peaceful">Peaceful Civic Protest</option>
                    </select>
                </div>

                {/* Map Visualization */}
                <div style={mapContainerStyle}>
                    {loading && <div style={overlayStyle}>Fetching latest data...</div>}
                    <MapContainer 
                        center={DEFAULT_CENTER} 
                        zoom={DEFAULT_ZOOM} 
                        style={mapStyle} 
                        scrollWheelZoom={false}
                    >
                        <TileLayer
                            attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
                            url="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
                        />
                        
                        {filteredAlerts.map((alert, index) => (
                            <Marker 
                                key={index} 
                                position={[alert.latitude, alert.longitude]}
                            >
                                <Popup>
                                    <strong style={{color: getRiskColor(alert.risk_score)}}>{alert.threat_type} (Risk: {alert.risk_score.toFixed(2)})</strong><br/>
                                    Action: {alert.recommended_action}<br/>
                                    Source: {alert.source_type}
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            </div>

            {/* 4. LIVE ALERT TABLE (Paginated) */}
            <h2 style={tableSectionTitleStyle}>
                Detailed Real-Time Alerts ({totalAlerts})
            </h2>
            <div style={{ overflowX: 'auto' }}>
                <table style={tableStyle}>
                    <thead>
                        <tr style={tableHeaderRowStyle}>
                            <th style={tableHeaderCellStyle}>Time</th>
                            <th style={tableHeaderCellStyle}>Risk Score</th>
                            <th style={tableHeaderCellStyle}>Threat Type</th>
                            <th style={tableHeaderCellStyle}>Source</th>
                            <th style={tableHeaderCellStyle}>Recommended Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {/* Use paginatedAlerts */}
                        {paginatedAlerts.map((alert, index) => (
                            <tr key={index} style={tableRowStyle}>
                                <td style={tableCellStyle}>{new Date(alert.timestamp * 1000).toLocaleTimeString()}</td>
                                <td style={{ ...tableCellStyle, color: getRiskColor(alert.risk_score), fontWeight: 'bold' }}>{alert.risk_score.toFixed(2)}</td>
                                <td style={tableCellStyle}>{alert.threat_type}</td>
                                <td style={tableCellStyle}>{alert.source_type}</td>
                                <td style={tableCellStyle}>{alert.recommended_action}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* 5. Pagination Controls */}
            <PaginationControls 
                totalItems={totalAlerts}
                itemsPerPage={ITEMS_PER_PAGE}
                currentPage={currentPage}
                onPageChange={setCurrentPage}
            />
        </div>
    );
};

// --- STYLED OBJECTS ---

const dashboardContainerStyle = { 
    padding: '30px', 
    backgroundColor: COLORS.BG_PRIMARY, 
    color: 'white', 
    minHeight: '100vh', 
    margin: '0 auto', 
    maxWidth: '1400px',
    fontFamily: 'system-ui, sans-serif'
};
const headerStyle = { 
    display: 'flex', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    marginBottom: '40px',
    padding: '0 10px'
};
const titleStyle = { 
    color: COLORS.ACCENT_LIGHT, 
    fontSize: '2.5em', 
    margin: 0, 
    fontWeight: 800,
    letterSpacing: '1px'
};
const signOutButtonStyle = { 
    padding: '12px 20px', 
    backgroundColor: COLORS.UI_CARD, 
    color: COLORS.TEXT_MUTED, 
    border: `1px solid ${COLORS.TEXT_MUTED}30`, 
    borderRadius: '6px', 
    cursor: 'pointer', 
    transition: '0.2s',
    fontSize: '0.9em'
};

const kpiRowStyle = { 
    display: 'grid', 
    gridTemplateColumns: 'repeat(3, 1fr)', 
    gap: '30px', // Increased gap for space
    marginBottom: '40px' 
};
const cardStyle = { 
    backgroundColor: COLORS.UI_CARD, 
    padding: '25px', 
    borderRadius: '10px', 
    position: 'relative', 
    textAlign: 'left', 
    minHeight: '140px',
    boxShadow: '0 6px 12px rgba(0,0,0,0.4)', // Deeper shadow
    border: `1px solid ${COLORS.UI_CARD}aa`
};
const kpiTitleStyle = { color: COLORS.TEXT_MUTED, margin: '0', fontSize: '1em' };
const kpiValueStyle = { margin: '15px 0 0 0', fontSize: '3em', fontWeight: 900 };
const kpiIconStyle = { fontSize: '40px', position: 'absolute', top: '20px', right: '20px', opacity: 0.7 };

const mainRowStyle = { display: 'flex', gap: '30px', textAlign: 'left' };
const sidebarStyle = { 
    width: '300px', 
    backgroundColor: COLORS.UI_CARD, 
    padding: '25px', 
    borderRadius: '10px', 
    flexShrink: 0,
    boxShadow: '0 6px 12px rgba(0,0,0,0.4)',
    height: 'fit-content'
};
const sidebarTitleStyle = { color: COLORS.ACCENT_LIGHT, borderBottom: '1px solid #333', paddingBottom: '10px', marginBottom: '15px', fontSize: '1.4em', fontWeight: 600 };
const labelStyle = { display: 'block', marginTop: '20px', color: COLORS.TEXT_MUTED, fontSize: '0.95em' };
const rangeInputStyle = { width: '100%', marginTop: '10px', WebkitAppearance: 'none', appearance: 'none', height: '10px', background: COLORS.BG_PRIMARY, borderRadius: '5px', cursor: 'pointer' };
const dropdownStyle = { width: '100%', padding: '12px', marginTop: '10px', borderRadius: '6px', border: '1px solid #444', backgroundColor: COLORS.BG_PRIMARY, color: 'white', fontSize: '1em' };
const mapContainerStyle = { flexGrow: 1, position: 'relative', height: '600px', borderRadius: '10px', overflow: 'hidden', boxShadow: '0 6px 12px rgba(0,0,0,0.4)' };
const overlayStyle = { position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.8)', zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center', color: COLORS.ACCENT_LIGHT, fontSize: '1.8em' };
const mapStyle = { height: '100%', width: '100%' };

const tableSectionTitleStyle = { color: COLORS.ACCENT_LIGHT, margin: '50px 0 20px 0', fontSize: '2em', textAlign: 'left', borderBottom: `1px solid ${COLORS.UI_CARD}`, paddingBottom: '10px', fontWeight: 600 };
const tableStyle = { width: '100%', borderCollapse: 'collapse', textAlign: 'left', backgroundColor: COLORS.UI_CARD, borderRadius: '8px', overflow: 'hidden', boxShadow: '0 6px 12px rgba(0,0,0,0.4)' };
const tableHeaderRowStyle = { backgroundColor: '#35374a', borderBottom: `2px solid ${COLORS.ACCENT_LIGHT}` };
const tableHeaderCellStyle = { padding: '18px 15px', textAlign: 'left', color: COLORS.ACCENT_LIGHT, fontWeight: 'bold', fontSize: '1.05em' };
const tableRowStyle = { transition: 'background-color 0.1s', borderBottom: `1px solid #333` };
const tableCellStyle = { padding: '15px', textAlign: 'left', fontSize: '0.95em' };

const paginationContainerStyle = { display: 'flex', justifyContent: 'center', padding: '20px 0', gap: '10px' };
const pageButtonStyle = (isActive) => ({
    padding: '8px 15px',
    backgroundColor: isActive ? COLORS.ACCENT_LIGHT : COLORS.UI_CARD,
    color: isActive ? COLORS.BG_PRIMARY : COLORS.TEXT_MUTED,
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontWeight: 'bold',
    transition: '0.2s'
});

export default Dashboard;