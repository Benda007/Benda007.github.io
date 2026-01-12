-- table with employees drinking coffee. I am thinking about manual setting up of main employees
-- while leaving possibility to manually modify the list.
    -- maybe via some external list? e.g. csv file etc..
CREATE TABLE employees (
    "id" INTEGER,
    "department_id" INTEGER,
    "name" TEXT NOT NULL,
    "surname" TEXT NOT NULL,
    "email" TEXT,
    "nickname" TEXT,
    "active" INTEGER NOT NULL DEFAULT 1, -- 1 = active, 0 = inactive
    PRIMARY KEY ("id"),
    FOREIGN KEY ("department_id") REFERENCES "departments"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE (email)
);


-- table with different departments. It is not physical location but more like a names of teams in the office - location
CREATE TABLE departments (
    "id" INTEGER,
    "name" TEXT NOT NULL,                   -- e.g., 'PUR1', 'MFE SERIAL', 'SW development' etc.. so more departments can be in one office
    "office_id" INTEGER NOT NULL,           -- which office/location this department belongs to
    "active" INTEGER NOT NULL DEFAULT 1,    -- 1 = active, 0 = inactive department
    PRIMARY KEY ("id"),
    FOREIGN KEY ("office_id") REFERENCES "locations"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE ("name", "office_id")            -- department names must be unique per office so they do not mix
);


-- table with coffee types. This can be limited for pre-defined types, or as in my case, left for checking by consumption table.
CREATE TABLE coffee_types (
    "id" INTEGER,
    "type" TEXT NOT NULL, -- CHECK ("type" IN ('espresso', 'lungo', 'lungo & extra water', 'americano')) this was not used afater all...
    UNIQUE ("type"),
    PRIMARY KEY ("id")
);

-- location of the coffee machine. This is actually list of machines and where are physically placed.
CREATE TABLE locations (
    "id" INTEGER ,
    "name" TEXT NOT NULL,
    "office" TEXT,
    PRIMARY KEY ("id"),
    UNIQUE ("name", "office")
);

-- table with a list of coffee machines. So we know basic information about coffe machine itself.
CREATE TABLE machines (
    "id" INTEGER,
    "location_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,       -- e.g., "DeLonghi", "Bosch"
    "serial" TEXT NOT NULL,     -- help to identify exact machine
    "active" INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY ("location_id") REFERENCES "locations"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    PRIMARY KEY ("id"),
    UNIQUE ("name", "serial")    -- this will ensure that one name of machine cannot have same serial number
);


-- Tracks when machines need maintenance based on number of cups made
-- Example: DeLonghi might need service every 500 cups, Jura every 1000 cups or so...
CREATE TABLE maintenance_tracking (
    "id" INTEGER,
    "machine_id" INTEGER NOT NULL,
    "cups_threshold" INTEGER NOT NULL,      -- how many cups before maintenance is needed. For every machine this will be different.
    "last_maintenance" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "cups_since_maintenance" INTEGER NOT NULL DEFAULT 0,  -- counter: number of cups made since last service
    "active" INTEGER NOT NULL DEFAULT 1,    -- 1 = active tracking, 0 = disabled
    PRIMARY KEY ("id"),
    FOREIGN KEY ("machine_id") REFERENCES "machines"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE ("machine_id")                   -- one maintenance tracking record per machine, more maintanance plants can't be done simultenously
);


-- simple table combining who did drink what coffee and when
CREATE TABLE consumption (
    "id" INTEGER,
    "employee_id" INTEGER NOT NULL,
    "coffee_id" INTEGER NOT NULL,
    "machine_id" INTEGER NOT NULL,
    "cost_id" INTEGER NOT NULL,
    "timestamp" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- "cost" REAL CHECK ("cost" >=0),
    PRIMARY KEY ("id"),
    FOREIGN KEY ("employee_id") REFERENCES "employees"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY ("coffee_id") REFERENCES "coffee_types"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY ("machine_id") REFERENCES "machines"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY ("cost_id") REFERENCES "costs"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- table of "costs of the coffee" because it can happen that costs of coffee changes in the time because
    -- coffee beans can be more or less expensive and also because each department is buying at different prices, or maintenace costs varies per machine

CREATE TABLE costs (
    "id" INTEGER,
    "cost" REAL CHECK ("cost" >=0),
    "coffee_id" INTEGER,
    "office_id" INTEGER,
    "timestamp" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id"),
    FOREIGN KEY ("office_id") REFERENCES "locations"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY ("coffee_id") REFERENCES "coffee_types"("id")
        ON UPDATE CASCADE ON DELETE RESTRICT,
    UNIQUE ("cost", "coffee_id", "office_id")
);

-- indexes based on data in database.
--  First one is indexing who (what emploees) are drinking cofee. This index should increase speed for viewing these data.
CREATE INDEX "consumption_employee_index" ON
"consumption"(employee_id, timestamp);


-- improving speed when viewing consumption per machine
CREATE INDEX "consumption_machine_time_index" ON
"consumption"(machine_id, timestamp);

-- improving speed of reading when viewing / working with consumption of the coffee
CREATE INDEX "consumption_coffee_index" ON
"consumption" (coffee_id, timestamp);

-- Speed up maintenance queries (find machines needing service)
CREATE INDEX "maintenance_status_index" ON
"maintenance_tracking"("machine_id", "cups_since_maintenance");

-- ======== views - showing some basic analysis
-- what type of coffee is most popular per day?
CREATE VIEW view_daily_type_popularity AS
SELECT
    DATE(timestamp) AS "day",
    "coffee_types"."type",
    COUNT(*) AS "cups"
FROM "consumption"
JOIN "coffee_types" ON "coffee_types"."id" = "coffee_id"
GROUP BY "day", "coffee_types"."type";

-- what was daily consumption of cofee per day per employ, showed as a number of cups.
    -- Then groupued per day and employee id. Considering to show also names.
CREATE VIEW daily_summary AS
SELECT
    DATE(timestamp) AS "day",
    "employee_id",
    COUNT(*) AS "cups"
FROM "consumption" GROUP BY "day", "employee_id";


