-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Started with this query to find the report that refers to this crime
SELECT id, description
FROM crime_scene_reports
WHERE street LIKE 'Humphrey%' AND day = 28;

