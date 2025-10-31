import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load .env from mongodb folder
dotenv.config({ path: path.resolve(__dirname, '../.env') });
const uri = process.env.MONGODB_URI;
console.log("Connecting to:", uri);


import { MongoClient } from 'mongodb';


const client = new MongoClient(uri);

async function insertSampleData() {
  try {
    await client.connect();
    console.log("Connected to earthquake_risk_db");
    const db = client.db('earthquake_risk_db');

    const locationResult = await db.collection('locations').insertOne({
      latitude: -1.957875,
      longitude: 30.112735,
      region: 'Kigali',
      ocean_proximity: false,
      created_at: new Date()
    });

    const monitoringResult = await db.collection('seismic_monitoring').insertOne({
      nst: 45,
      dmin: 0.12,
      gap: 180.5,
      cdi: 4,
      mmi: 5,
      data_quality_score: 0.87,
      created_at: new Date()
    });

    const tsunamiResult = await db.collection('tsunami_events').insertOne({
      tsunami: false,
      risk_level: 'Low',
      predicted_probability: 0.05,
      impact_assesment: 'Minimal impact expected',
      created_at: new Date(),
      updated_at: new Date()
    });

    const earthquakeResult = await db.collection('earthquakes').insertOne({
      location_id: locationResult.insertedId,
      monitoring_id: monitoringResult.insertedId,
      tsunami_id: tsunamiResult.insertedId,
      magnitude: 4.8,
      depth: 10.5,
      sig: 120,
      Year: 2025,
      Month: 10,
      created_at: new Date(),
      updated_at: new Date()
    });

    await db.collection('earthquake_audit_log').insertOne({
      table_name: 'earthquakes',
      operation: 'insert',
      record_id: earthquakeResult.insertedId,
      old_values: null,
      new_values: {
        magnitude: 4.8,
        depth: 10.5,
        sig: 120,
        Year: 2025,
        Month: 10
      },
      changed_at: new Date(),
      changed_by: 'admin_user'
    });

    console.log("Sample data inserted successfully!");
  } catch (error) {
    console.error("Error inserting data:", error);
    if (error.errInfo?.details?.schemaRulesNotSatisfied) {
      console.dir(error.errInfo.details.schemaRulesNotSatisfied, { depth: null });
    }
  } finally {
    await client.close();
    console.log("Connection closed.");
  }
}

insertSampleData();