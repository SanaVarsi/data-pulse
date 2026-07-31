SELECT
    date,
    ROUND(AVG(temperature_c), 2)      AS avg_temp_c,
    ROUND(MAX(temperature_c), 2)      AS max_temp_c,
    ROUND(MIN(temperature_c), 2)      AS min_temp_c,
    ROUND(AVG(wind_speed_kmh), 2)     AS avg_wind_speed_kmh,
    ROUND(MAX(wind_speed_kmh), 2)     AS max_wind_speed_kmh,
    ROUND(SUM(precipitation_mm), 2)   AS total_precipitation_mm,
    ROUND(AVG(cloud_cover_pct), 1)    AS avg_cloud_cover_pct,
    COUNT(*)                          AS hour_count
FROM {{ ref('silver_weather') }}
GROUP BY date
ORDER BY date