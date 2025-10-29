-- Stored Procedures for Earthquake-Tsunami Database

-- Function to calculate tsunami risk based on earthquake parameters
CREATE OR REPLACE FUNCTION calculate_tsunami_risk(
    p_magnitude FLOAT,
    p_depth FLOAT,
    p_latitude FLOAT,
    p_longitude FLOAT
) RETURNS VARCHAR(20) AS $$
DECLARE
    risk_level VARCHAR(20);
    ocean_nearby BOOLEAN := FALSE;
BEGIN
    -- Simple ocean proximity check (can be enhanced)
    ocean_nearby := (ABS(p_longitude) > 30 OR ABS(p_latitude) < 60);
    
    -- Calculate risk based on magnitude, depth, and ocean proximity
    IF p_magnitude >= 8.5 AND p_depth <= 50 AND ocean_nearby THEN
        risk_level := 'EXTREME';
    ELSIF p_magnitude >= 7.5 AND p_depth <= 100 AND ocean_nearby THEN
        risk_level := 'HIGH';
    ELSIF p_magnitude >= 6.8 AND p_depth <= 200 AND ocean_nearby THEN
        risk_level := 'MEDIUM';
    ELSE
        risk_level := 'LOW';
    END IF;
    
    RETURN risk_level;
END;
$$ LANGUAGE plpgsql;

-- Function to get earthquake statistics by year
CREATE OR REPLACE FUNCTION get_yearly_earthquake_stats(p_year INT)
RETURNS TABLE(
    total_earthquakes BIGINT,
    avg_magnitude FLOAT,
    max_magnitude FLOAT,
    tsunami_events BIGINT,
    tsunami_percentage FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) as total_earthquakes,
        AVG(e.magnitude) as avg_magnitude,
        MAX(e.magnitude) as max_magnitude,
        SUM(CASE WHEN te.tsunami THEN 1 ELSE 0 END) as tsunami_events,
        (SUM(CASE WHEN te.tsunami THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as tsunami_percentage
    FROM earthquakes e
    JOIN tsunami_events te ON e.tsunami_id = te.tsunami_id
    WHERE e.Year = p_year;
END;
$$ LANGUAGE plpgsql;