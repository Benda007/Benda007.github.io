# Coffee Consumption Tracker

A normalized SQLite database and reporting toolkit for tracking office coffee usage across multiple locations and departments. Built as the final project for Harvard's CS50 SQL course.

**[Video Walkthrough](https://youtu.be/oizss0OHE-U)** | **[Design Document](DESIGN.md)**

---

## Overview

This project demonstrates practical database design principles through a real-world use case: tracking coffee consumption in multi-location offices. The system records *who* drinks *what* coffee from *which* machine *when*, enabling cost analysis, usage pattern discovery, and predictive maintenance planning.

### Core Purpose

The database serves five main goals:
1. **Record consumption**: Every time someone drinks coffee, capture employee, coffee type, machine, and timestamp
2. **Track costs**: Store prices per office with timestamps to preserve historical pricing
3. **Plan maintenance**: Monitor machine usage based on cup count rather than time-based schedules
4. **Analyze by department**: Understand which departments drink the most coffee and spending patterns
5. **Find patterns**: Answer questions like "what time do most people drink coffee?" and "which coffee is most popular?"

---

## Key Design Features

### ✓ Normalized Schema (3NF)
Eliminates data redundancy through proper table decomposition. Each entity has a single source of truth.

### ✓ Historical Price Tracking
Cost records include timestamps, so consumption always references the price in effect at purchase time—even if prices change later. This prevents historical data corruption and enables temporal cost analysis.

### ✓ Usage-Based Maintenance Planning
Maintenance thresholds are tracked per machine based on actual cup count, not arbitrary time-based schedules. The `maintenance_tracking` table records cups consumed since last service.

### ✓ Referential Integrity
- Foreign key constraints ensure data consistency
- Cascade/restrict rules prevent orphaned records
- Departments require valid offices; machines require valid locations

### ✓ Performance Optimization
**Four strategic indexes:**
- `consumption_employee_index` — fast employee history lookups
- `consumption_machine_time_index` — machine usage patterns  
- `consumption_coffee_index` — coffee type popularity analysis
- `maintenance_status_index` — maintenance due queries

**Two pre-built views:**
- `view_daily_type_popularity` — daily coffee type popularity
- `daily_summary` — cups per employee per day

---

## Database Schema

### Core Tables (8 total)

| Table | Purpose |
|-------|---------|
| `employees` | Staff with department assignment and active status |
| `departments` | Organizational teams tied to offices |
| `locations` | Office codes and specific spots (kitchen, entrance, etc.) |
| `machines` | Coffee machines with serial numbers assigned to locations |
| `coffee_types` | Available coffee varieties |
| `consumption` | Main transaction log: who drank what, when, from where, and cost |
| `costs` | Price history per coffee type per office (with timestamps) |
| `maintenance_tracking` | Machine maintenance schedules based on cup count |

### Key Design Insights

**Locations Structure:**
The `locations` table stores office names/codes (like "PUR", "FIN", "R&D") as TEXT in the `office` field alongside specific spot names (like "kitchen", "entrance"). This allows multiple spots within each office while preventing duplicate spot names within the same office.

**Price History:**
Costs are referenced by `cost_id` in consumption records, not as direct prices. When a price changes, a new cost record is created—the old record remains, creating an immutable price history. This ensures:
- No duplication of price data
- Historical accuracy—old records never lose their original price
- Temporal analysis—queries can track price changes across time

**Machine Immutability:**
Once a machine is assigned to a location, it stays there. If a machine physically moves, a new database record is created, maintaining clean historical data and preventing relationship corruption.

**Employee Department:**
Each employee has exactly one `department_id`. When someone changes departments, that field updates—but previous consumption records are not retroactively reassigned. This is a documented design tradeoff.

---

## How It Works

### Recording a Coffee Purchase

When an employee drinks coffee, a single INSERT captures the transaction while preserving price history:

```sql
INSERT INTO consumption (employee_id, coffee_id, machine_id, cost_id)
VALUES (
  1,
  2,
  3,
  (
    SELECT id FROM costs
    WHERE coffee_id = 2 AND office_id = 1
    ORDER BY timestamp DESC
    LIMIT 1
  )
);
```

The `cost_id` lookup automatically finds the current price for that coffee in that office, ensuring historical accuracy.

### Common Analytical Queries

**Most popular coffee today:**
```sql
SELECT ct.type, COUNT(*) AS cups
FROM consumption c
JOIN coffee_types ct ON c.coffee_id = ct.id
WHERE date(c.timestamp) = date('now')
GROUP BY ct.type
ORDER BY cups DESC;
```

**Department spending:**
```sql
SELECT d.name, SUM(c.cost) AS total_spent
FROM consumption con
JOIN costs c ON con.cost_id = c.id
JOIN employees e ON con.employee_id = e.id
JOIN departments d ON e.department_id = d.id
WHERE date(con.timestamp) = date('now')
GROUP BY d.name;
```

**Machines approaching maintenance:**
```sql
SELECT m.name, m.serial, mt.cups_since_maintenance, mt.cups_threshold
FROM machines m
JOIN maintenance_tracking mt ON m.id = mt.machine_id
WHERE mt.cups_since_maintenance >= mt.cups_threshold * 0.9
  AND mt.active = 1;
```

---

## Project Scope

### What This Database Does
✓ Record consumption with employee, coffee type, machine, timestamp, and historical price  
✓ Track price changes over time per office  
✓ Monitor machine usage for predictive maintenance  
✓ Analyze consumption by employee, department, machine, and time period  
✓ Generate reports on coffee popularity, spending, and maintenance schedules  

### What It Does NOT Do
✗ No automated alerts or notifications  
✗ No web interface or payment processing  
✗ No real-time inventory management  
✗ No automatic maintenance counter updates (manual SQL UPDATE required)  
✗ No multi-department employee assignments (matrix organizations not supported)  
✗ No machine movement tracking between locations  
✗ No historical department membership for employees  

See **[DESIGN.md](DESIGN.md)** for detailed limitations and tradeoffs.

---

## Getting Started

### Prerequisites
- SQLite3 (command line or IDE like DB Browser for SQLite)
- Basic SQL knowledge

### Setup Steps

1. **Create schema:** Run `schema.sql` to initialize all tables, indexes, and views
2. **Load sample data:** Insert initial records for employees, locations, departments, and machines
3. **Define costs:** Add price records for each coffee type in each office
4. **Start tracking:** Insert consumption records as employees drink coffee
5. **Query the data:** Run queries or use the pre-built views

### Example Workflow

```bash
# Open SQLite
sqlite3 coffee.db

# Load schema and create all tables
.read schema.sql

# Query the pre-built summary view
SELECT * FROM daily_summary;
```

---

## Learning Outcomes

This project demonstrates:

**Database Design Principles:**
- Third Normal Form (3NF) and eliminating redundancy
- Entity-Relationship modeling with proper cardinality
- Foreign key constraints and referential integrity
- Indexing strategies for query performance

**Advanced SQL Concepts:**
- Temporal data handling (price history with timestamps)
- Foreign key lookups in INSERT statements
- Aggregate functions (COUNT, SUM, GROUP BY)
- Multiple JOINs across normalized tables
- View creation for query abstraction

**Real-World Data Modeling:**
- Handling organizational hierarchies (locations → departments → employees)
- Designing for immutable historical records
- Implementing usage-based thresholds
- Handling temporal complexity (price changes over time)

---

## Technical Specifications

| Aspect | Details |
|--------|---------|
| **Database** | SQLite3 |
| **Schema Normalization** | 3NF (Third Normal Form) |
| **Timezone Handling** | UTC for consistency and portability |
| **Constraints** | PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK |
| **Indexes** | 4 indexes on high-frequency queries |
| **Views** | 2 pre-built views for common reports |
| **Language** | Pure SQL (no ORM or application layer) |

---

## Project Files

```
CS50_SQL_project/
├── README.md           # This file
├── DESIGN.md           # Comprehensive design document
├── schema.sql          # Database schema (tables, indexes, views)
├── queries.sql         # Example analytical queries
├── erd_diagram.png     # Entity-relationship diagram
└── coffee.db           # SQLite database file
```

---

## Documentation

- **[DESIGN.md](DESIGN.md)** — In-depth design covering scope, functional requirements, schema details, relationships, optimizations, and limitations
- **[Video Walkthrough](https://youtu.be/oizss0OHE-U)** — Live demonstration of the database and key queries

---

## About This Project

**Course:** Harvard CS50 SQL — Introduction to SQL  
**Project Type:** Final project demonstrating database design, normalization, and SQL analysis  

This project showcases practical application of relational database principles in a realistic scenario with multiple stakeholders, temporal complexity (price history), and analytical requirements.

---

## License

MIT License

---

## Questions or Feedback?

Feel free to open an issue or contact the author. This project is open-sourced as part of my professional portfolio to demonstrate database design expertise.
