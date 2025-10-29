# Global Earthquake-Tsunami Risk Assessment Database Documentation

## Overview
This database is designed to store and analyze earthquake and tsunami data. It helps API developers, ML engineers, and other users access structured data for their tasks.

## Key Features
- **Normalized Schema**: Data is organized to avoid duplication.
- **Audit Logging**: Tracks changes to earthquake data.
- **Stored Procedures**: Includes tsunami risk calculation and yearly statistics.
- **Triggers**: Automatically updates timestamps and logs changes.

## Tables
### 1. Earthquakes
Stores earthquake details.
| Column         | Type              | Description                              |
|----------------|-------------------|------------------------------------------|
| earthquake_id  | SERIAL            | Unique ID for each earthquake.           |
| location_id    | INTEGER           | Links to `locations` table.              |
| monitoring_id  | INTEGER           | Links to `seismic_monitoring` table.     |
| tsunami_id     | INTEGER           | Links to `tsunami_events` table.         |
| magnitude      | DOUBLE PRECISION  | Richter scale magnitude.                 |
| depth          | DOUBLE PRECISION  | Depth of the earthquake in kilometers.   |
| sig            | INTEGER           | Significance score.                      |
| Year           | INTEGER           | Year of occurrence.                      |
| Month          | INTEGER           | Month of occurrence.                     |
| created_at     | TIMESTAMP         | Record creation time.                    |
| updated_at     | TIMESTAMP         | Last update time.                        |

### 2. Locations
Stores geographic data.
| Column       | Type      | Description                  |
|--------------|-----------|------------------------------|
| location_id  | SERIAL    | Unique ID for each location. |
| latitude     | FLOAT     | Latitude of the location.    |
| longitude    | FLOAT     | Longitude of the location.   |

### 3. Seismic Monitoring
Stores monitoring data.
| Column         | Type              | Description                              |
|----------------|-------------------|------------------------------------------|
| monitoring_id  | SERIAL            | Unique ID for monitoring data.           |
| nst            | INTEGER           | Number of stations detecting the event.  |
| dmin           | FLOAT             | Distance to the nearest station.         |
| gap            | FLOAT             | Azimuthal gap between stations.          |
| cdi            | INTEGER           | Community Decimal Intensity.             |
| mmi            | INTEGER           | Modified Mercalli Intensity.             |

### 4. Tsunami Events
Stores tsunami-specific data.
| Column       | Type      | Description                  |
|--------------|-----------|------------------------------|
| tsunami_id   | SERIAL    | Unique ID for each tsunami.  |
| tsunami      | BOOLEAN   | Whether a tsunami occurred.  |

### 5. Earthquake Audit Log
Tracks changes to earthquake data.
| Column       | Type      | Description                  |
|--------------|-----------|------------------------------|
| log_id       | SERIAL    | Unique ID for each log entry.|
| table_name   | VARCHAR   | Name of the table changed.   |
| operation    | VARCHAR   | Type of operation (INSERT, UPDATE, DELETE). |
| record_id    | INTEGER   | ID of the affected record.   |
| old_values   | JSONB     | Previous values.             |
| new_values   | JSONB     | New values.                  |
| changed_at   | TIMESTAMP | Time of change.              |
| changed_by   | VARCHAR   | User who made the change.    |

## Stored Procedures
### 1. `calculate_tsunami_risk`
Calculates tsunami risk based on earthquake parameters.
- **Input**: `magnitude`, `depth`, `latitude`, `longitude`
- **Output**: Risk level (`LOW`, `MEDIUM`, `HIGH`, `EXTREME`)
- **Example**: `SELECT calculate_tsunami_risk(7.8, 25.0, 35.0, 140.0);`

### 2. `get_yearly_earthquake_stats`
Provides yearly earthquake statistics.
- **Input**: `year`
- **Output**: Total earthquakes, average magnitude, max magnitude, tsunami events, tsunami percentage.
- **Example**: `SELECT * FROM get_yearly_earthquake_stats(2021);`

## Triggers
### 1. `earthquake_audit_trigger`
Logs changes to the `earthquakes` table.
- **Event**: `AFTER INSERT, UPDATE, DELETE`
- **Example Log Entry**: `SELECT * FROM earthquake_audit_log ORDER BY changed_at DESC LIMIT 1;`

### 2. `earthquakes_update_timestamp`
Updates the `updated_at` column automatically.
- **Event**: `BEFORE UPDATE`

## Example Queries
### 1. Count Tsunamis by Year
```sql
SELECT e."Year", COUNT(*) as total, SUM(CASE WHEN te.tsunami THEN 1 ELSE 0 END) as tsunamis
FROM earthquakes e
JOIN tsunami_events te ON e.tsunami_id = te.tsunami_id
GROUP BY e."Year"
ORDER BY e."Year";
```

### 2. Join All Tables
```sql
SELECT e.magnitude, e.depth, l.latitude, l.longitude, sm.nst, sm.cdi, te.tsunami
FROM earthquakes e
JOIN locations l ON e.location_id = l.location_id
JOIN seismic_monitoring sm ON e.monitoring_id = sm.monitoring_id
JOIN tsunami_events te ON e.tsunami_id = te.tsunami_id
LIMIT 10;
```

## Connection Details
- **Host**: `<your-database-host>`
- **Port**: `5432`
- **Database Name**: `postgres`
- **Username**: `postgres`
- **Password**: `<your-password>`

## Notes
- Share this documentation with API developers and ML engineers.
- Use the example queries and procedures for integration.