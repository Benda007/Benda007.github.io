-- insert a new coffee into table "coffee_types"
INSERT INTO "coffee_types" ("type")
VALUES  ('espresso'),
        ('lungo'),
        ('americano'),
        ('capucino');


-- insert new locations of coffee machines with name of place within given office
INSERT INTO "locations" ("name", "office")
VALUES  ('at entrance', 'PUR'),
        ('kitchen', 'FIN'),
        ('at assistant', 'Director'),
        ('meeting point', 'R&D'),
        ('loby', 'R&D');


-- insert a new records into "machines" table so we do have coffee machines ready for coffee lovers
INSERT INTO "machines" ("location_id", "name", "serial", "active")
VALUES  ('1', 'DeLonghi', '153785', '1'),
        ('2', 'Bosch standard', '856314', '1'),
        ('3', 'Jura', '567952', '1'),
        ('4', 'DeLonghi', '864382', '0'),
        ('5', 'Jura master class', '159853', '1');

-- insert new records for coffee costs into "costs" table
INSERT INTO "costs" ("cost", "coffee_id", "office_id")
VALUES  ('6', '1', '1'),
        ('6', '2', '1'),
        ('6', '3', '1'),
        ('6', '1', '2'),
        ('6', '2', '2'),
        ('6', '3', '2'),
        ('5', '1', '3'),
        ('5', '2', '3'),
        ('5', '3', '3'),
        ('8', '1', '4'),
        ('8', '2', '4'),
        ('8', '3', '4'),
        ('7', '1', '5'),
        ('7', '2', '5'),
        ('7', '3', '5');

-- insert departments for each office
INSERT INTO "departments" ("name", "office_id")
VALUES  ('PUR1', 1),
        ('PUR2', 1),
        ('PUR QUALITY', 1),
        ('PUR HQ', 1),
        ('FIN BUDGETING', 2),
        ('FIN ACCOUNTING', 2),
        ('ELS DESIGN', 4),
        ('PLASTIC DESIGN', 4),
        ('SW DEVELOPMENT', 4),
        ('STANDARTISATION TEAM', 5),
        ('RECEPTION', 3);


-- insert a new record into table "employees" with all required inputs.
INSERT INTO "employees" ("name", "surname", "email", "nickname", "department_id")
VALUES  ('Robert', 'Murphy', 'bob.murphy@domain.com', 'Bob', 1),
        ('John', 'Lenon', 'johnlennon@beatle.co.uk', 'John Onno', 8),
        ('Paul', 'McCartney', 'johnmccartney@beatle.co.uk', 'Paul The Beatle', 9),
        ('Ringo', 'Star', 'ringo@beatle.co.uk', 'Mr.Ringo', 5),
        ('George', 'Harrison', 'georgeh@beatle.co.uk', 'humble George', 6),
        ('Bob', 'Marley', 'b0b@hairy.jm', 'Marley', 10);

-- very manual ==== insert a new record into table "consumption" with all required inputs. replaced by following query
-- INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id") -- where to find cost_id
-- VALUES ('2', '1', '1', '2');
-- ('2', '1', '2', '1'),
-- ('1', '2', '4', '2'),
-- ('4', '1', '2', '3'),
-- ('2', '2', '1', '1');

-- ==== this is more automated version with costs whicH is searching for coffee costs in costs table per coffee type and machine location
        -- but it is working only with one row, need an improvement.
-- INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
-- VALUES ('2', '1', '1',  (SELECT "costs"."id"
--         FROM "costs"
--         JOIN "coffee_types" ON "coffee_types"."id" = "costs"."coffee_id"
--         WHERE "costs"."office_id" = (
--         SELECT "machines"."location_id"
--         FROM "machines"
--         JOIN "locations" ON "machines"."location_id" = "locations"."id"
--         WHERE "machines"."id" = 3) AND "coffee_types"."id" = 1)
--         );

-- final version of inserting into consumption ==== UNION ALL: Each pair of coffee_id and machine_id is listed
-- using SELECT statements combined with UNION ALL.
        -- This way, it can be created a derived table named input that the main query can reference.
        -- this was found on google
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 1 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 1 AS coffee_id, 1 AS machine_id UNION ALL -- UNION ALL I found in internet w3schools, very interesting solution of my problem
    SELECT 1, 2 UNION ALL
    SELECT 2, 1 UNION ALL
    SELECT 1, 3
) AS input;

-- this is just to input similar records for different user 2
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 2 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 1 AS coffee_id, 3 AS machine_id UNION ALL
    SELECT 3, 2 UNION ALL
    SELECT 1, 3
) AS input;

-- this is just to input similar records for different user 3
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 3 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 3 AS coffee_id, 3 AS machine_id UNION ALL
    SELECT 2, 2 UNION ALL
    SELECT 1, 4
) AS input;


-- this is just to input similar records for different user 4
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 4 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 2 AS coffee_id, 5 AS machine_id UNION ALL
    SELECT 2, 3 UNION ALL
    SELECT 2, 3
) AS input;

-- this is just to input similar records for different user 5
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 5 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 1 AS coffee_id, 5 AS machine_id UNION ALL
    SELECT 1, 2 UNION ALL
    SELECT 1, 5
) AS input;

-- this is just to input similar records for different user 6
INSERT INTO "consumption" ("employee_id", "coffee_id", "machine_id", "cost_id")
SELECT 6 AS "employee_id", input.coffee_id, input.machine_id,
    (SELECT "costs"."id"
     FROM "costs"
     WHERE "costs"."office_id" = (
         SELECT "machines"."location_id"
         FROM "machines"
         WHERE "machines"."id" = input.machine_id)
     AND "costs"."coffee_id" = input.coffee_id) AS "cost_id"
FROM (
    SELECT 2 AS coffee_id, 2 AS machine_id UNION ALL
    SELECT 3, 1 UNION ALL
    SELECT 2, 4
) AS input;


-- subqueries for above insert queries - helping queries
-- SELECT "machines"."location_id"
-- FROM "machines"
-- JOIN "locations" ON "machines"."location_id" = "locations"."id"
-- WHERE "machines"."id" = 1;

-- SELECT "costs"."id"
-- FROM "costs"
-- JOIN "coffee_types" ON "coffee_types"."id" = "costs"."coffee_id"
-- WHERE "costs"."office_id" = 1 AND "coffee_types"."id" = 1;

-- insert maintenance tracking for each machine
-- set different thresholds based on machine type and usage expectations
INSERT INTO "maintenance_tracking" ("machine_id", "cups_threshold", "last_maintenance")
VALUES  (1, 200, CURRENT_TIMESTAMP),      -- DeLonghi at entrance: service every 200 cups
        (2, 250, CURRENT_TIMESTAMP),     -- Bosch standard: service every 250 cups
        (3, 200, CURRENT_TIMESTAMP),      -- Jura: service every 200 cups
        (4, 400, CURRENT_TIMESTAMP),      -- DeLonghi private: service every 400 cups (inactive but tracked)
        (5, 500, CURRENT_TIMESTAMP);     -- Jura Master class - strong machine with longer maintenance interval for 500 cups

--=========--
-- update "employees" table to change nickname
    -- very simple exampe of usage update on employees table
UPDATE "employees"
SET "nickname" = 'Robert'
WHERE "nickname" = 'Bob';

-- update timestamp for user_id 2
    -- this is used for simulation of different time consumption, so the later views are a bit more meaningfull. To spread consumption in a day.
UPDATE "consumption"
SET "timestamp" = strftime('%Y-%m-%d ', "timestamp") || '23' || strftime(':%M:%S', "timestamp")
WHERE "employee_id" = 2;
-- same as above, for user_id 4
UPDATE "consumption"
SET "timestamp" = strftime('%Y-%m-%d ', "timestamp") || '13' || strftime(':%M:%S', "timestamp")
WHERE "employee_id" = 4;

-- update "employees" table to change status to inactive for specific employee_id
UPDATE "employees"
SET "active" = 0
WHERE "id" = 3 AND "active" = 1;

-- update coffee "machines" table to set machine active
UPDATE "machines"
SET "active" = 0
WHERE "id" = 2 AND "active" = 1;

-- update coffee "machines" table to change name of machine with id = 2
UPDATE "machines"
SET "name" = "Bosch Big Machine"
WHERE "id" = 2;

-- update locations table by changing name of the machine or office
UPDATE "locations"
SET "office" = 'MFE'
WHERE "id" = 3;

UPDATE "locations"
SET "name" = 'kitchen'
WHERE "id" = 3;




--=============
-- analytics queries
-- select hour extracted from timestamp and COUNT(*) grouped by hour. This should give us peak coffee hours.
-- peak hours for coffee drinkers
SELECT COUNT (strftime('%H', "timestamp")) AS 'Coffee peak count', strftime('%H', "timestamp") AS 'Rush hour'
FROM "consumption"
GROUP BY (strftime('%H', "timestamp"));



-- daily coffee consumption per employee_id and name
-- SELECT DATE(timestamp), employee_id, COUNT(*) grouped by day and employee_id. Hope this will give required consuption per person
SELECT "daily_summary"."day" AS 'Date', "daily_summary"."employee_id" AS 'Employee id', "employees"."nickname" AS 'Employee nickname',
    "daily_summary"."cups" AS 'Number of cups'
FROM "daily_summary"
JOIN "employees" ON "employees"."id" = "daily_summary"."employee_id"
GROUP BY "daily_summary"."day", "daily_summary"."employee_id"
ORDER BY "daily_summary"."cups" DESC, "daily_summary"."day";

--===========

-- show consumption of coffee type per name with timestamp, here day in a month
SELECT "employees"."name" AS 'Name', "employees"."surname" AS 'Surname',
        "coffee_types"."type" AS 'Coffee', strftime('%m-%d', "timestamp") AS 'Month and Day'
FROM "employees"
JOIN "consumption" ON "employees"."id" = "consumption"."employee_id"
JOIN "coffee_types" ON "coffee_types"."id" = "consumption"."coffee_id"
ORDER BY strftime('%m-%d', "timestamp");

-- show consumption by machine location
-- join consumption, machines, and locations to display day, coffee type, and location name.
SELECT "machines"."name" AS 'Name', "locations"."office" AS 'Office',
    COUNT("consumption"."coffee_id") AS 'Cups',
    CAST(ROUND(SUM("costs"."cost"), 0) AS INTEGER) AS 'Coffee cost' -- interesting way how to achive number without decimal point. Found on w3school
FROM "machines"
JOIN "locations" ON "locations"."id" = "machines"."location_id"
JOIN "costs" ON "consumption"."cost_id" = "costs"."id"
JOIN "consumption" ON "consumption"."machine_id" = "machines"."id"
GROUP BY "locations"."office", "machines"."name";


-- show consumption by machine location
-- joining consumption, machines, and locations to display total counts by machine and office.
SELECT "machines"."name" AS 'Name of the machine', "locations"."office" AS 'Office', "coffee_types"."type" AS 'Coffee type',
    COUNT("consumption"."coffee_id") AS 'Cups',
    CAST(COALESCE(SUM("costs"."cost"), 0) AS INTEGER) AS 'Coffee cost'  -- COALESCE can handle NULLs on top of SUM. Very nice!
FROM "machines"
JOIN "consumption" ON "consumption"."machine_id" = "machines"."id"
JOIN "locations" ON "locations"."id" = "machines"."location_id"
JOIN "coffee_types" ON "coffee_types"."id" = "consumption"."coffee_id"
LEFT JOIN "costs" ON "consumption"."cost_id" = "costs"."id"  -- change to LEFT JOIN - This allows me to keep all consumption records,
                                                                -- even if they do not have associated cost entries, making output represent
                                                                -- actual consumption. I had to google it a bit.
GROUP BY "machines"."name", "locations"."office", "coffee_types"."type";

-- update cups_since_maintenance counter (needs to be run periodically)
    -- this counts actual cups made since last maintenance and then a maintenance tracker will show real status for maintenenace.
UPDATE "maintenance_tracking"
SET "cups_since_maintenance" = (
    SELECT COUNT("consumption"."id")
    FROM "consumption"
    WHERE "consumption"."machine_id" = "maintenance_tracking"."machine_id"
    AND "consumption"."timestamp" > COALESCE("maintenance_tracking"."last_maintenance", '1970-01-01') -- strong support of google for this logic was needed
);


-- maintenance tracker - based o info from maintenance_table this query should
    -- show a table - overview which machines needs cleaning and when
SELECT "machines"."name" AS 'Name of the machine', "locations"."office" AS 'Office', "maintenance_tracking"."cups_since_maintenance" AS 'Cups since maintenance',
        "maintenance_tracking"."cups_threshold" AS 'Cups treshold', ("maintenance_tracking"."cups_threshold" - "maintenance_tracking"."cups_since_maintenance") AS 'Cups till maintenance threshold',
        "maintenance_tracking"."cups_since_maintenance" * 100 / "maintenance_tracking"."cups_threshold" AS 'Percentage to maintenance'

FROM "maintenance_tracking"
JOIN "machines" ON "maintenance_tracking"."machine_id" = "machines"."id"
JOIN "locations" ON "locations"."id" = "machines"."location_id"
ORDER BY ("maintenance_tracking"."cups_since_maintenance" * 100 / "maintenance_tracking"."cups_threshold") DESC;


-- resetting maintanece threshold for selected machine, when the maintenance will be really done. Here example for machine_id 1
UPDATE "maintenance_tracking"
SET "last_maintenance" = CURRENT_TIMESTAMP, "cups_since_maintenance" = 0
WHERE "machine_id" IN (1,2,3,4,5);  -- Change machine_id as needed

