WITH rolling_stats AS (
    SELECT
        date,
        avg_temp_c,
        AVG(avg_temp_c) OVER (
            ORDER BY date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_avg,
        STDDEV_SAMP(avg_temp_c) OVER (
            ORDER BY date
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ) AS rolling_stddev
    FROM {{ ref('gold_weather_daily') }}
)
SELECT
    date,
    avg_temp_c,
    rolling_avg,
    rolling_stddev,
    CASE
        WHEN rolling_stddev > 0
        THEN (avg_temp_c - rolling_avg) / rolling_stddev
        ELSE 0
    END AS z_score,
    CASE
        WHEN rolling_stddev > 0
        AND ABS((avg_temp_c - rolling_avg) / rolling_stddev) > 2
        THEN true
        ELSE false
    END AS is_anomaly
FROM rolling_stats
ORDER BY date
