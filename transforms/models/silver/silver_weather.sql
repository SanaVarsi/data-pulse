SELECT
    CAST(timestamp AS TIMESTAMP)                    AS timestamp,
    DATE_TRUNC('hour', CAST(timestamp AS TIMESTAMP)) AS hour,
    CAST(timestamp AS DATE)                          AS date,
    CAST(temperature AS DOUBLE)                      AS temperature_c,
    CAST(wind_speed AS DOUBLE)                       AS wind_speed_kmh,
    CAST(wind_direction AS INTEGER)                  AS wind_direction_deg,
    CAST(precipitation AS DOUBLE)                    AS precipitation_mm,
    CAST(cloud_cover AS INTEGER)                     AS cloud_cover_pct,
    LOWER(TRIM(condition))                           AS condition,
    source_id
FROM {{ ref('bronze_weather') }}
WHERE timestamp IS NOT NULL