-- Keep a log of any SQL queries you execute as you solve the mystery.

/* The theft took place on July 28, 2023 at 10:15am on Humphrey Street bakery */

-- Started with this query to find the report that refers to this crime
SELECT id, description
FROM crime_scene_reports
WHERE street LIKE '%Humphrey%' AND day = 28;

-- Returns the transcripts of the interviews made at the day of theft to learn what witnesses saw
SELECT name, transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;

/* Ruth, Eugene and Raymond are the supposed witnesses
   Ruth seems to be telling the truth about seeing the thief run away in a car from the bakery parking lot.
   Eugene sounds weird saying that she recognized the thief, and that he was withdrawing money
    just before the robery. (is Emma the owner of the bakery?)
   Raymond sounds suspitious as well because he says the thief was saying out loud
    what was his escape plan right after the robery took place.
    (is Raimond saying 'they' thinking of the accomplice?) */

-- Check security logs for owners of veicules that exited the bakery after the theft
SELECT name, hour, minute, activity, people.license_plate FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

SELECT '';

-- Check calls log for the lead about the thief call after the theft that were less than a minute
SELECT * FROM
(SELECT name, phone_number, duration FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60) c1
LEFT JOIN
(SELECT name, phone_number, duration FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60) c2
ON c1.name = c2.name;


-- Searches for the atm transaction that the witness saw
SELECT DISTINCT name, transaction_type FROM people
JOIN bank_accounts ON person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2023 AND month = 7 AND day = 28
AND atm_location LIKE '%Leggett%' AND transaction_type = 'withdraw';


SELECT '';

-- The query below returns 4 names that exited the parking lot
-- between 10h15-10h25 and also made a call roughly at the same period for less than a minute
DROP VIEW IF EXISTS conc;
CREATE VIEW conc AS
SELECT DISTINCT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE bakery_security_logs.year = 2023 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25
AND duration < 60;

SELECT * FROM conc;

SELECT '';

-- This one checks all of the above informations against each other to see if there is a match
SELECT DISTINCT name, people.id FROM people
JOIN bank_accounts ON person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location LIKE '%Leggett%' AND transaction_type = 'withdraw'
AND people.name IN (SELECT * FROM conc);

SELECT '';

/* Above query didn't returned any result, so that maybe confirms my suspection with Eugene's testimony? */

-- Shows which of the previous suspects' traveled on the next day
SELECT t1.name, origin, id, destination FROM
(SELECT name, full_name AS origin, flights.id FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE name IN (SELECT * FROM conc)
AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29) t1

INNER JOIN

(SELECT name, full_name AS destination FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
JOIN airports ON flights.destination_airport_id = airports.id
WHERE name IN (SELECT * FROM conc)
AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29) t2

ON t1.name = t2.name;

SELECT '';

SELECT * FROM phone_calls
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;