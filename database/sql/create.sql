-- Global Earthquake-Tsunami Risk Assessment Database Schema
-- PostgreSQL Implementation for Supabase

-- Create Locations Table
CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
    region VARCHAR(100),
    ocean_proximity BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Seismic Monitoring Table
CREATE TABLE IF NOT EXISTS seismic_monitoring (
    monitoring_id SERIAL PRIMARY KEY,
    nst INT NOT NULL CHECK (nst >= 0),
    dmin FLOAT CHECK (dmin >= 0),
    gap FLOAT CHECK (gap >= 0 AND gap <= 360),
    cdi INT CHECK (cdi >= 0 AND cdi <= 9),
    mmi INT CHECK (mmi >= 1 AND mmi <= 9),
    data_quality_score FLOAT CHECK (data_quality_score >= 0 AND data_quality_score <= 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Tsunami Events Table
CREATE TABLE IF NOT EXISTS tsunami_events (
    tsunami_id SERIAL PRIMARY KEY,
    tsunami BOOLEAN NOT NULL,
    risk_level VARCHAR(20) DEFAULT 'UNKNOWN',
    predicted_probability FLOAT CHECK (predicted_probability >= 0 AND predicted_probability <= 1),
    impact_assessment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Earthquakes Table (Main table)
CREATE TABLE IF NOT EXISTS earthquakes (
    earthquake_id SERIAL PRIMARY KEY,
    location_id INT REFERENCES locations(location_id) ON DELETE CASCADE,
    monitoring_id INT REFERENCES seismic_monitoring(monitoring_id) ON DELETE SET NULL,
    tsunami_id INT REFERENCES tsunami_events(tsunami_id) ON DELETE CASCADE,
    magnitude FLOAT NOT NULL CHECK (magnitude >= 0 AND magnitude <= 10),
    depth FLOAT NOT NULL CHECK (depth > 0),
    sig INT NOT NULL CHECK (sig > 0),
    Year INT NOT NULL CHECK (Year >= 1900 AND Year <= EXTRACT(YEAR FROM CURRENT_DATE)),
    Month INT NOT NULL CHECK (Month >= 1 AND Month <= 12),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Earthquake Audit Log Table
CREATE TABLE IF NOT EXISTS earthquake_audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    changed_by VARCHAR(100) DEFAULT CURRENT_USER
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_earthquakes_magnitude ON earthquakes(magnitude);
CREATE INDEX IF NOT EXISTS idx_earthquakes_year ON earthquakes(Year);
CREATE INDEX IF NOT EXISTS idx_earthquakes_year_month ON earthquakes(Year, Month);
CREATE INDEX IF NOT EXISTS idx_locations_coordinates ON locations(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_tsunami_occurred ON tsunami_events(tsunami);
CREATE INDEX IF NOT EXISTS idx_monitoring_nst ON seismic_monitoring(nst);
CREATE INDEX IF NOT EXISTS idx_audit_table_name ON earthquake_audit_log(table_name);
CREATE INDEX IF NOT EXISTS idx_audit_changed_at ON earthquake_audit_log(changed_at);

-- Add comments to tables for documentation
COMMENT ON TABLE earthquakes IS 'Main table storing earthquake event data';
COMMENT ON TABLE locations IS 'Geographic information for earthquake epicenters';
COMMENT ON TABLE seismic_monitoring IS 'Seismic monitoring and measurement data';
COMMENT ON TABLE tsunami_events IS 'Tsunami occurrence and risk assessment data';
COMMENT ON TABLE earthquake_audit_log IS 'Audit trail for database changes';