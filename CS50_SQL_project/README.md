# Coffee Consumption Tracker

## Overview

This project tracks coffee consumption across various office locations and departments. It allows logging of details such as who drinks coffee, which type, from which machine, and at what time, helping organizations analyze usage patterns and manage resources effectively.

## Features

- **Record Consumption**: Logs each coffee consumption event, including employee, coffee type, machine, and timestamp.
- **Cost Tracking**: Monitors coffee prices across different offices, allowing for price change analysis.
- **Maintenance Planning**: Alerts users when machines require maintenance based on actual usage.
- **Department Analysis**: Identifies coffee consumption trends by department.
- **Usage Patterns**: Provides insights into peak consumption times and popular coffee types.

## Database Structure

### Entities

- **Employees**: Information about employees, such as names, email, and department.
- **Locations**: Details about office locations and specific spots for coffee machines.
- **Departments**: Teams within offices.
- **Machines**: Information regarding coffee machines and their statuses.
- **Coffee Types**: Different types of coffee available.
- **Consumption**: Records of each coffee consumption event.
- **Costs**: Historical pricing information for each coffee type.
- **Maintenance Tracking**: Details about maintenance schedules based on machine usage.

### Relationships

- A single office can have multiple departments and machines.
- Each machine serves many consumption events linked to individual employees.

## Usage

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/CoffeeConsumptionTracker.git


2. Set up the database using SQL scripts provided in queries.sql.

Running Queries

Refer to queries.sql for predefined queries to interact with the database, ensuring correct cost records are linked to consumption.

## Limitations

- **No Complex Cost Validation**: When recording consumption, there's no built-in mechanism to prevent incorrect cost assignments (e.g., recording espresso costs as 8 euros instead of 6). Queries in `queries.sql` help mitigate this issue by using careful INSERT statements to look up the correct cost automatically.
  
- **No Timezone Conversion**: All timestamps are stored in UTC. If you're in Prague (CET), a consumption at 9:00 AM shows as 8:00 AM in the database. To resolve this, convert timestamps from UTC to local time when displaying them.

- **No Deletion of Records**: Once a consumption record is created, it cannot be deleted. Mistakes can be corrected by updating the record or inserting a correcting record instead.

- **Lack of Notes or Comments**: The current design does not allow for attaching notes to records, such as marking a consumption as part of a training event. It is advised to maintain external documentation for any additional context.

- **Manual Maintenance Tracking**: Maintenance counters are updated manually; this means someone must run an UPDATE query to recalculate it. If this is neglected, the counter may become inaccurate.

## Summary

The Coffee Consumption Tracker is a functional database system for monitoring coffee consumption across various departments. It demonstrates key database design principles such as normalization and referential integrity. While it has limitations, such as lack of automatic alerts or advanced historical tracking, it serves as an educational tool showcasing the concepts learned in CS50 SQL.

## Acknowledgments

Developed by Jean Kocman  
For additional support or inquiries, please contactby mail [(Jean.Kocman@seznam.cz)].

