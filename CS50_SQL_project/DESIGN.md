# Design Document

By Jean Kocman

Video overview: <https://youtu.be/oizss0OHE-U>

## Scope

### Purpose

This database tracks coffee consumption in an office with multiple locations and departments. The main goal is to record who drinks what coffee, from which machine, and when. This helps understand coffee usage patterns, manage machine maintenance based on actual usage, track costs, and answer questions like "which coffee is most popular?" or "which machine needs service soon?"

The database has five main purposes:

1. **Record consumption**: Every time someone drinks coffee, we record the employee, coffee type, machine, and timestamp
2. **Track costs**: Coffee prices are different in different offices, so we store costs separately and can track how prices change over time
3. **Plan maintenance**: Instead of maintaining machines on a schedule, we track how many cups each machine makes and alert when maintenance is needed
4. **Analyze by department**: We can see which departments drink the most coffee and how much it costs
5. **Find patterns**: We can answer questions like "what time do most people drink coffee?" or "which coffee type is most popular?"

### What is included

**People**: Employees with their names, email, nickname, and which department they work in

**Places**: Office locations (like PUR, FIN, R&D) and specific spots within those offices (like kitchen, entrance)

**Departments**: Teams within offices (like PUR1, PUR2, SW DEVELOPMENT). Multiple departments can be in the same office

**Things**: Coffee machines with their location and serial number; types of coffee available; each coffee consumption record with a timestamp; maintenance information for each machine; cost information for each coffee type in each office

**Time data**: Every consumption record and maintenance action has a timestamp so we can see when things happened

### What is NOT included

**Machine details**: We don't store technical specs like power, size, or model year. Only the brand name, serial number, and location

**Employee personal information**: We only store name, surname, email, nickname, and department. No address, phone, salary, or hire date

**Supplies/inventory**: We don't track coffee beans, water, cups, or stock levels

**Money handling**: This is not a payment system. We track costs for analysis, but don't handle actual payments or invoices

**Repair details**: We don't track which technician fixed a machine, what was fixed, or repair costs. Only when maintenance happened

**Employee preferences**: We can see what coffee each person drinks, but we don't store favorite coffee, allergies, or ratings

**Machine moving between locations**: Once a machine is in a location, we assume it stays there. If it moves, it would need a new record

**Employees changing departments**: When someone moves to a different department, we update their record, but we don't keep a history of which department they were in before


## Functional Requirements

### What users can do with this database

1. **Add and update employees**: Create new employee records, change their information, mark them as inactive when they leave
2. **Manage departments**: Create new departments within offices, activate or deactivate them
3. **Manage machines**: Add machines to the system, assign them to locations, update their status, track their serial numbers
4. **Define coffee types**: Add new types of coffee (espresso, cappuccino, etc.)
5. **Define locations**: Create office names and specific spot names within each office
6. **Set and update costs**: Store coffee prices for each coffee type in each office, update prices when they change
7. **Record consumption**: When someone drinks coffee, record it with employee, type, machine, and cost
8. **Track maintenance**: Set how many cups each machine should make before maintenance (500 cups, 1000 cups, etc.), record when maintenance was done, and track current status
9. **Query consumption data**: Look up who drank what, when they drank it, from which machine, and how much it cost
10. **Generate reports**:
    - What time of day do people drink most coffee?
    - How much coffee does each employee drink per day?
    - Which coffee types are most popular?
    - Which machines are used most and how much do they cost?
    - Which machines need maintenance soon?
    - How much does each department spend on coffee?

### What this database does NOT do

- It does NOT automatically send alerts or notifications
- It does NOT prevent going over budget
- It does NOT have a web or mobile interface—only SQL queries
- It does NOT track who entered the data into the system
- It does NOT automatically count cups or update maintenance counters—that needs to be done with UPDATE queries


## Representation

### Entities

An entity is a thing we want to store information about. Here are the tables in this database:

![Entity Relationship Diagram](erd_diagram.png)


#### **employees**

**What it stores**: Information about the people who drink coffee

**Columns**:
- `id`: A number that uniquely identifies each employee (like an employee number)
- `department_id`: Which department the employee works in
- `name`: First name
- `surname`: Last name
- `email`: Email address
- `nickname`: A nickname or informal name (optional)
- `active`: Is this employee still working? (1 = yes, 0 = no)

**Why these types**:
- We split name and surname into two fields instead of one combined field. This makes it easier to sort by surname or search by last name independently
- Email is TEXT because SQLite doesn't have an EMAIL type, but we mark it UNIQUE so no two employees have the same email
- Nickname is optional (can be empty) because some people don't have informal names
- Active is 0 or 1 (not true/false) because SQLite doesn't have a boolean type. 1 means active, 0 means inactive

**Why these constraints**:
- PRIMARY KEY makes sure each employee has a unique number
- NOT NULL on name, surname, and department_id means we require these fields—we always need to know an employee's basic info
- UNIQUE on email prevents two people from having the same email address
- DEFAULT 1 on active means new employees are marked as active automatically
- FOREIGN KEY to departments makes sure an employee can only be assigned to a department that exists

#### **departments**

**What it stores**: The teams or groups within offices

**Columns**:
- `id`: Unique number for each department
- `name`: Department name (like "PUR1", "SW DEVELOPMENT", "MFE SERIAL")
- `office_id`: Which office this department belongs to
- `active`: Is this department still active? (1 = yes, 0 = no)

**Why these types**:
- Name is TEXT to allow flexible naming conventions
- Office_id is a number (foreign key) rather than the office name as text. This way, if the office name changes, we only update it in one place

**Why these constraints**:
- PRIMARY KEY gives each department a unique number
- NOT NULL on name and office_id means we always need these values
- UNIQUE("name", "office_id") means we can't have two departments with the same name in the same office, but we CAN have the same name in different offices. For example, there could be a "PUR1" in the PUR office and a different "PUR1" structure in another office (though in practice this might not happen)
- FOREIGN KEY makes sure departments can only be assigned to offices that exist
- The CASCADE and RESTRICT rules: CASCADE means if an office name is updated, the departments automatically use the new name. RESTRICT means we can't delete an office if there are departments in it

#### **locations**

**What it stores**: The office locations where coffee machines are

**Columns**:
- `id`: Unique number for each location
- `name`: The specific spot name (like "kitchen", "entrance", "meeting room")
- `office`: The office name or code (like "PUR", "FIN", "R&D")

**Why these types**:
- Both name and office are TEXT
- Together they describe where the machine is (in which office, and in which room/spot)

**Why these constraints**:
- PRIMARY KEY gives each location a unique number
- UNIQUE("name", "office") means we can have multiple "kitchen" locations as long as they're in different offices. But we can't have two "kitchen" locations in the PUR office
- NOT NULL on name means every location needs a description

#### **machines**

**What it stores**: Information about the actual coffee machines

**Columns**:
- `id`: Unique number for each machine
- `location_id`: Which location this machine is in
- `name`: Brand or model name (like "DeLonghi", "Bosch", "Jura")
- `serial`: Serial number for identification (every physical machine has a unique serial number)
- `active`: Is this machine in use? (1 = yes, 0 = no, meaning retired)

**Why these types**:
- Serial is TEXT because serial numbers often have letters or special characters, not just numbers
- Name is TEXT
- Active is 0 or 1 following the pattern used elsewhere in the database

**Why these constraints**:
- PRIMARY KEY gives each machine a unique number
- NOT NULL on location_id, name, and serial means we always need these values
- UNIQUE("name", "serial") means we can't register the exact same machine twice. Different machines can have the same brand name, but not the same serial number
- FOREIGN KEY makes sure machines can only be in locations that exist
- CASCADE allows location updates; RESTRICT prevents deleting locations if machines are still there

#### **coffee_types**

**What it stores**: The different types of coffee available

**Columns**:
- `id`: Unique number for each coffee type
- `type`: The coffee name (like "espresso", "cappuccino", "americano")

**Why these types**:
- Type is TEXT to allow different naming styles

**Why these constraints**:
- PRIMARY KEY gives each coffee type a unique number
- UNIQUE on type means we can't have two entries for "espresso"
- NOT NULL means we always need a coffee name
- We kept this table simple because coffee types change slowly and are easy to add

#### **consumption**

**What it stores**: Every time someone drinks coffee—this is the main transaction record

**Columns**:
- `id`: Unique number for each consumption event
- `employee_id`: Which employee drank the coffee
- `coffee_id`: What type of coffee
- `machine_id`: Which machine they used
- `cost_id`: How much did it cost (stored as a reference to the costs table, not as a direct number)
- `timestamp`: When did they drink it? (automatically filled with current time)

**Why these types**:
- Timestamp is automatically set to the current time in UTC (CURRENT_TIMESTAMP). We use UTC because it doesn't change based on time zones, which makes testing and data consistency easier
- Cost is stored as a foreign key (cost_id) instead of a direct price number. This is important because prices change! By storing a reference to the costs table, we can see what the actual price was when the coffee was consumed, even if prices changed later

**Why these constraints**:
- PRIMARY KEY makes each consumption event unique
- NOT NULL on timestamp means we always know when something was consumed
- FOREIGN KEYs connect consumption to employees, coffee types, machines, and costs—this ensures we can't record consumption without these pieces of data existing first
- RESTRICT means you can't delete an old consumption record. This keeps historical data safe

**Why is cost separate?**: This is an important design choice. We could have stored the price directly in consumption, but that would be bad because:
1. **Avoids repetition**: If espresso costs 6 euros in the PUR office, storing "6" for every espresso consumed in PUR would be wasteful
2. **Tracks price changes**: When prices change, a separate costs table lets us know what the actual price was at the time. A consumption record from 3 months ago can still reference the price that was in effect then
3. **Better queries**: We can answer questions like "how much did coffee cost each month?" without confusion

#### **costs**

**What it stores**: The price of each coffee type in each office (with history of price changes)

**Columns**:
- `id`: Unique number for each cost record
- `cost`: The price per cup (a decimal number like 6.50)
- `coffee_id`: Which coffee type this price is for
- `office_id`: Which office this price applies to
- `timestamp`: When was this price set? (automatically filled with current time)

**Why these types**:
- Cost is REAL (not INTEGER) because prices have decimals (6.50, not just 6)
- Timestamp is automatic so we know when prices were recorded

**Why these constraints**:
- PRIMARY KEY makes each cost record unique
- NOT NULL on coffee_id and office_id means we always know what and where
- CHECK(cost >= 0) prevents negative prices (can't have a negative cost!)
- UNIQUE("cost", "coffee_id", "office_id") prevents duplicate entries. But importantly, this allows NEW records when the price CHANGES. For example, if espresso was 6 euros, then changed to 7 euros, we can store both records
- FOREIGN KEYs connect to coffee types and offices, ensuring we can't set a price for a non-existent coffee or office
- Timestamp tracks when each price was set, creating a price history

#### **maintenance_tracking**

**What it stores**: Information about when machines need maintenance, based on how many cups they've made

**Columns**:
- `id`: Unique number for each maintenance record
- `machine_id`: Which machine this is for
- `cups_threshold`: How many cups before maintenance is needed? (like 500 or 1000)
- `last_maintenance`: When was the machine last serviced?
- `cups_since_maintenance`: How many cups has the machine made since the last service? (a counter)
- `active`: Is this machine being tracked? (1 = yes, 0 = no)

**Why these types**:
- Cups_threshold and cups_since_maintenance are INTEGER because you count cups as whole numbers, not decimals
- Last_maintenance is TIMESTAMP to record when service was done
- Active is 0 or 1

**Why these constraints**:
- PRIMARY KEY makes each maintenance record unique
- NOT NULL on machine_id and cups_threshold means we always need these values
- UNIQUE on machine_id means each machine has exactly one maintenance tracking record. A machine can't have conflicting maintenance schedules
- FOREIGN KEY to machines ensures we only track machines that exist
- RESTRICT prevents deleting machines that have maintenance tracking
- DEFAULT 0 on cups_since_maintenance starts the counter at zero

**How it works in practice**: When a machine is first set up, we record it with cups_threshold = 500 (example). As employees drink coffee from that machine, the cups_since_maintenance counter goes up. When the counter reaches 500, maintenance is due. After maintenance, we update last_maintenance to the current date and reset cups_since_maintenance back to 0. The counter starts counting again.

### Relationships

Here's how the tables connect to each other:

**Locations → Departments** (one office has many departments):
- One office (like PUR) can have many departments (PUR1, PUR2, QUALITY, HQ)
- Each department belongs to exactly one office

**Locations → Machines** (one location has many machines):
- One spot can have multiple machines
- Each machine is in exactly one location

**Departments → Employees** (one department has many employees):
- One department (like SW DEVELOPMENT) has many employees
- Each employee works in exactly one department

**Employees → Consumption** (one employee has many coffee consumptions):
- One employee can drink many coffees over time
- Each consumption event is by exactly one employee

**Coffee Types → Consumption** (one type appears in many consumptions):
- Espresso can be consumed many times
- Each consumption event is exactly one coffee type

**Machines → Consumption** (one machine serves many consumptions):
- One machine makes many cups over time
- Each consumption event is from exactly one machine

**Costs → Consumption** (one cost applies to many consumptions):
- The cost record for "espresso in PUR office = 6 euros" applies to many espresso consumptions
- Each consumption event links to exactly one cost record

**Coffee Types → Costs** (one type has multiple prices over time):
- Espresso might cost 6 euros now, but cost 5 euros 6 months ago
- So there are multiple cost records for the same coffee type

**Locations → Costs** (one office has many price records):
- PUR office might have one price for espresso, FIN office a different price
- Each cost record applies to one office

**Machines → Maintenance Tracking** (one machine has one maintenance record):
- Each machine has exactly one maintenance tracking record
- That record is for exactly one machine

In visual form, the most important relationships look like this:

```
Office/Location (1) ──── many (N) Machines
                    ──── many (N) Departments
                                      │
                                      └── many (N) Employees
                                                      │
                                                      └── many (N) Consumption Events


Coffee Type (1) ──── many (N) Consumption Events
            ──── many (N) Cost Records (because prices change)

Machine (1) ──── one (1) Maintenance Tracking Record
```


## Optimizations

### Indexes

An index is like a table of contents in a book. Without it, you have to read every page. With an index, you can jump directly to the section you want. Database indexes speed up queries.

#### **consumption_employee_index**

**What it does**: Makes queries about a specific employee's coffee drinking history faster

**Query example**: "Show all coffee consumed by employee John over the past week"

**Why it helps**: Without this index, the database would have to read through every consumption record to find John's entries. With the index, it can jump directly to his records and check dates quickly.

**How it works**: The index organizes records first by employee_id, then by timestamp. So all of John's records are together, in time order.

#### **consumption_machine_time_index**

**What it does**: Makes queries about machine usage patterns faster

**Query example**: "How much was machine #1 used each day?"

**Why it helps**: This index lets the database quickly find all usage of a specific machine and organize it by date.

#### **consumption_coffee_index**

**What it does**: Makes queries about coffee type popularity faster

**Query example**: "Which coffee was most popular today?"

**Why it helps**: The index quickly finds all records of a specific coffee type, grouped by time.

#### **maintenance_status_index**

**What it does**: Makes maintenance status queries faster

**Query example**: "Which machines need maintenance soon?"

**Why it helps**: This index helps quickly find machines that are approaching their maintenance threshold.

### Views

A view is like a saved query. Instead of writing the same complicated query every time, you save it as a view and just query the view.

#### **view_daily_type_popularity**

**What it shows**: Which coffee types were most popular each day

**Example output**:
- Day 2025-12-10: espresso 5 cups, cappuccino 3 cups, americano 2 cups
- Day 2025-12-11: cappuccino 4 cups, espresso 3 cups, americano 3 cups

**Why it's useful**: Instead of writing a complex GROUP BY query yourself, you can just ask: "SELECT * FROM view_daily_type_popularity WHERE day = '2025-12-11'"

#### **daily_summary**

**What it shows**: How many cups each employee drank each day

**Example output**:
- Day 2025-12-10: employee 1 = 2 cups, employee 3 = 1 cup, employee 5 = 3 cups
- Day 2025-12-11: employee 1 = 1 cup, employee 2 = 2 cups

**Why it's useful**: When combined with the employees table (using JOIN), you can see names: "Bob drank 2 cups on 2025-12-10"


## Limitations

Every database design has limitations and tradeoffs. Here are the main ones in this design:

### **1. Machines can't move between locations**

**The problem**: Once you assign a machine to a location, it stays there forever in the database. If you physically move a machine to a different office, you can't record this in the database.

**Why it's designed this way**: Machines are assumed to stay in one place. Supporting machine movement would make the database much more complicated.

**Real-world impact**: If you move a machine from PUR to FIN, you'd have to create a new machine record. This means your old records are tied to the old location.

**Solution**: If machines move, either keep detailed notes outside the database, or accept that historical records stay with the original location.

### **2. No history when employees change departments**

**The problem**: When an employee moves from one department to another, we update their current department. But we lose the record of which department they were in before.

**Real-world impact**: If Bob worked in PUR1 for 3 months, then moved to SW DEVELOPMENT, his old coffee consumption shows up in SW DEVELOPMENT records (because we updated his department), not in PUR1 records.

**Solution**: Don't change employee departments if you need accurate historical reports. Or keep notes about department changes outside the database.

### **3. Maintenance counter is manual**

**The problem**: The cups_since_maintenance counter is not automatic. Someone has to run an UPDATE query to recalculate it. If you forget, the counter becomes wrong.

**Why**: SQLite doesn't have automatic triggers like bigger database systems. Adding automatic updates would require more complex setup.

**Real-world impact**: If you don't update the counter regularly, you won't know when maintenance is actually due.

**Solution**: Create a weekly reminder to run the UPDATE query that recalculates the counter.

### **4. No budget limits**

**The problem**: The database tracks how much coffee costs, but doesn't prevent spending over budget. A department can spend as much as they want with no system warning.

**Why**: Enforcing budgets is more of an application feature than a database feature.

**Solution**: Generate monthly cost reports and check them against budgets manually.

### **5. No automatic alerts**

**The problem**: If a machine is due for maintenance or if unusual consumption happens, the database doesn't send an alert. You have to run queries manually to check.

**Why**: Sending alerts requires an application or script running outside the database.

**Solution**: Schedule someone to regularly run maintenance and consumption reports, or set up an external reporting tool.

### **6. Employees can only be in one department**

**The problem**: If someone works across multiple teams or in a matrix organization, the database doesn't support this well. They're assigned to exactly one department.

**Real-world impact**: A QA person who supports both R&D and production can't be properly tracked in this database.

**Solution**: Assign them to their primary department, or create separate employee records for each role.

### **7. Cost validation is weak**

**The problem**: When you record consumption, nothing prevents you from linking the wrong cost record. For example, you could record that espresso costs 8 euros, even though the actual cost record says 6 euros.

**Why**: SQLite doesn't support complex cross-table validation rules.

**Solution**: The queries provided in queries.sql use careful INSERT statements that look up the correct cost automatically. Use those patterns.

### **8. No timezone conversion**

**The problem**: All timestamps are stored in UTC. If you're in Prague (CET), a consumption at 9:00 AM shows as 8:00 AM in the database.

**Why**: Storing in UTC is a best practice for consistency and testing.

**Solution**: When displaying timestamps, you (or an application) can convert from UTC to local time.

### **9. Can't delete consumption records**

**The problem**: Once someone's coffee consumption is recorded, it can't be deleted. If you make a mistake, the record stays there forever.

**Why**: Deleting old data is dangerous. Keeping records preserves history and prevents accidental data loss.

**Solution**: If a record is wrong, you can update it (like changing which employee drank it), or insert a correcting record.

### **10. No notes or comments**

**The problem**: You can't attach notes to records. For example, you can't mark that a coffee consumption was "training event, not normal consumption" or add notes to a maintenance record.

**Why**: This database focuses on core tracking. A more complex system would have a notes field on many tables.

**Solution**: Keep external documentation (like spreadsheets or a notebook) for additional context.

---

## Summary

This Coffee Consumption Tracker is a useful system for tracking employee coffee usage across multiple offices and departments. The design uses proper database principles like normalization (avoiding repeated data) and referential integrity (making sure all data is connected correctly). Indexes make queries fast, and views simplify common reports. While it has some limitations (like no automatic alerts or perfect historical tracking), these are reasonable tradeoffs for an educational database project. The design demonstrates understanding of database concepts learned in CS50 SQL.


