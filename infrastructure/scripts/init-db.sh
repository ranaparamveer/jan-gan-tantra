#!/bin/bash
set -e

echo "Initializing Jan-Gan-Tantra database..."

# Enable PostGIS extension
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS postgis;
    CREATE EXTENSION IF NOT EXISTS postgis_topology;
    CREATE EXTENSION IF NOT EXISTS vector;
    
    -- Create spatial index for issues table (will be created by Django migrations)
    -- This is just a placeholder for future optimization
    
    SELECT PostGIS_version();
EOSQL

echo "Database initialization complete!"
