-- Keep a log of any SQL queries you execute as you solve the mystery.

/* Note: The theft took place on July 28, 2023 at 10:15am on Humphrey Street bakery */


-- Started with this query to find the report that may refer to this crime
SELECT id, description
FROM crime_scene_reports
WHERE description LIKE '%Humphrey%' AND day = 28;


-- This returns the transcripts of the interviews made at the day of theft to learn what witnesses saw
SELECT name, transcript FROM interviews WHERE year = 2023 AND month = 7 AND day = 28
AND transcript LIKE '%bakery%';


-- Check security logs for owners of veicules that exited the bakery after the theft
SELECT name, hour, minute, activity, people.license_plate FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25;

-- Check call logs folowing the lead about the thiefs call that lasted less than a minute
SELECT c1.id, c1.name caller, c1.phone_number, c2.name receiver, c2.phone_number FROM
(
    SELECT phone_calls.id, name, phone_number FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.caller
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
) c1
INNER JOIN
(
    SELECT phone_calls.id, name, phone_number, duration FROM people
    JOIN phone_calls ON people.phone_number = phone_calls.receiver
    WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60
) c2
ON c1.id = c2.id;

-- Searches for the atm transaction that the witness saw
SELECT DISTINCT name, transaction_type, atm_location FROM people
JOIN bank_accounts ON person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE year = 2023 AND month = 7 AND day = 28
AND atm_location LIKE '%Leggett%' AND transaction_type = 'withdraw';


-- The query below returns 4 names that exited the parking lot
-- between 10h15-10h25 and also made a call roughly at the same period for less than a minute
DROP VIEW IF EXISTS parking_and_call;
CREATE VIEW parking_and_call AS
SELECT DISTINCT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE bakery_security_logs.year = 2023 AND bakery_security_logs.month = 7 AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10 AND bakery_security_logs.minute >= 15 AND bakery_security_logs.minute <= 25
AND duration < 60;


-- This one checks all of the above informations against each other to see if there is a match
SELECT DISTINCT name FROM people
JOIN bank_accounts ON person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2023
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_location LIKE '%Leggett%' AND transaction_type = 'withdraw'
AND people.name IN (SELECT * FROM parking_and_call);


-- These shows which of the previous suspects' traveled on the next day
SELECT f1.name, origin, id, destination, f1.hour, f1.minute FROM
(
    SELECT name, full_name AS origin, flights.id, flights.hour, flights.minute FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    JOIN airports ON flights.origin_airport_id = airports.id
    WHERE name IN (SELECT * FROM parking_and_call)
    AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29
) f1
INNER JOIN
(
    SELECT name, full_name AS destination FROM people
    JOIN passengers ON people.passport_number = passengers.passport_number
    JOIN flights ON passengers.flight_id = flights.id
    JOIN airports ON flights.destination_airport_id = airports.id
    WHERE name IN (SELECT * FROM parking_and_call)
    AND flights.year = 2023 AND flights.month = 7 AND flights.day = 29
) f2

ON f1.name = f2.name;

/* Based on the last two queries' results, I think Bruce was the thief,
   he run away to LaGuardia Airport in New York (The first flight of July 29th),
   and Robin was his accomplice, as he called her after the robbery */
