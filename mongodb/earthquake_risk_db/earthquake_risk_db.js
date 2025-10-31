import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from mongodb folder
dotenv.config({ path: path.resolve(__dirname, '../.env') });

import { MongoClient, ObjectId } from 'mongodb';

// Connection URL
const uri = process.env.MONGODB_URI;

// Create new client
const client = new MongoClient(uri);

// Create and setup database
async function setupDatabase() {
    try {
        await client.connect();
        console.log("connected to MongoDB successfully");

        const db = client.db('earthquake_risk_db');
        console.log("Database earthquake_risk_db created successfully and selected");

        await db.createCollection("locations", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["latitude", "longitude"],
                    properties: {
                        latitude: { bsonType: "double", minimum: -90, maximum: 90 },
                        longitude: { bsonType: "double", minimum: -180, maximum: 180 },
                        region: { bsonType: "string" },
                        ocean_proximity: { bsonType: "bool" },
                        created_at: { bsonType: "date" }
                    }
                }
            }
        });
        console.log("Collection locations created successfully");

        await db.createCollection("seismic_monitoring", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["nst"],
                    properties: {
                        nst: { bsonType: "int", minimum: 0 },
                        dmin: { bsonType: "double", minimum: 0 },
                        gap: { bsonType: "double", minimum: 0, maximum: 360 },
                        cdi: { bsonType: "int", minimum: 0, maximum: 9 },
                        mmi: { bsonType: "int", minimum: 1, maximum: 9 },
                        data_quality_score: { bsonType: "double", minimum: 0, maximum: 1 },
                        created_at: { bsonType: "date" }
                    }
                }
            }
        });
        console.log("Collection seismic_monitoring created successfully");

        await db.createCollection("tsunami_events", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["tsunami"],
                    properties: {
                        tsunami: { bsonType: "bool" },
                        risk_level: { bsonType: "string" },
                        predicted_probability: { bsonType: "double", minimum: 0, maximum: 1 },
                        impact_assesment: { bsonType: "string" },
                        created_at: { bsonType: "date" },
                        updated_at: { bsonType: "date" }
                    }
                }
            }
        });
        console.log("Collection tsunami_events created successfully");

        await db.createCollection("earthquakes", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["location_id", "magnitude", "depth", "sig", "Year", "Month"],
                    properties: {
                        location_id: { bsonType: "objectId" },
                        monitoring_id: { bsonType: "objectId" },
                        tsunami_id: { bsonType: "objectId" },
                        magnitude: { bsonType: "double", minimum: 0, maximum: 10 },
                        depth: { bsonType: "double", minimum: 0 },
                        sig: { bsonType: "int", minimum: 0 },
                        Year: { bsonType: "int", minimum: 1900 },
                        Month: { bsonType: "int", minimum: 1, maximum: 12 },
                        created_at: { bsonType: "date" },
                        updated_at: { bsonType: "date" }
                    }
                }
            }
        });
        console.log("Collection earthquakes created successfully");

        await db.createCollection("earthquake_audit_log", {
            validator: {
                $jsonSchema: {
                    bsonType: "object",
                    required: ["table_name", "operation"],
                    properties: {
                        table_name: { bsonType: "string" },
                        operation: { bsonType: "string" },
                        record_id: { bsonType: "objectId" },
                        old_values: { bsonType: ["object", "null"] },
                        new_values: { bsonType: ["object", "null"] },
                        changed_at: { bsonType: "date" },
                        changed_by: { bsonType: "string" }
                    }
                }
            }
        });
        console.log("Collection earthquake_audit_log created successfully");

        console.log("All collections created with schema validation (data types)!");
    } finally {
        await client.close();
        console.log("Database setup complete and connection closed!");
    }
}

// Execution of the function
setupDatabase();