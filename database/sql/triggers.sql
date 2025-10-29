-- Triggers for Earthquake-Tsunami Database

-- Trigger function to automatically update timestamps
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger function for audit logging
CREATE OR REPLACE FUNCTION log_earthquake_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO earthquake_audit_log (table_name, operation, record_id, new_values)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.earthquake_id, row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO earthquake_audit_log (table_name, operation, record_id, old_values, new_values)
        VALUES (TG_TABLE_NAME, TG_OP, NEW.earthquake_id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO earthquake_audit_log (table_name, operation, record_id, old_values)
        VALUES (TG_TABLE_NAME, TG_OP, OLD.earthquake_id, row_to_json(OLD));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER earthquakes_update_timestamp
    BEFORE UPDATE ON earthquakes
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER tsunami_events_update_timestamp
    BEFORE UPDATE ON tsunami_events
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER earthquake_audit_trigger
    AFTER INSERT OR UPDATE OR DELETE ON earthquakes
    FOR EACH ROW EXECUTE FUNCTION log_earthquake_changes();