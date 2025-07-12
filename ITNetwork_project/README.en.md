<a href="README.en.md"><img src="https://em-content.zobj.net/thumbs/120/twitter/322/flag-united-kingdom_1f1ec-1f1e7.png" alt="English" width="30"/></a>
<a href="README.md"><img src="https://em-content.zobj.net/thumbs/120/twitter/322/flag-czechia_1f1e8-1f1ff.png" alt="Čeština" width="30"/></a>
# Insurance Policyholders Record

This project is the final test of a course organized by ITNetwork. It is a console application for managing the records of insurance policyholders, allowing users to add, display, search, and export data about policyholders.

## Project Files

- **`main.py`**: The main script that initializes the application and runs the main loop.
- **`insured.py`**: Contains the `InsuredPerson` class, which represents individual policyholders.
- **`insurance_agent.py`**: Contains the `InsuranceAgent` and `RecordData` classes, which handle the application logic and data manipulation for policyholders.

## Usage

Upon starting the program, you will have the following options:

1. **Add a new policyholder**: Enter a new policyholder's details. The program will verify the correctness of the entered information such as first name, last name, age (1-80 years), and phone number.
2. **List all policyholders**: Displays a list of all policyholders in a formatted manner for easier readability.
3. **Search for a policyholder**: Allows you to search for a specific policyholder by first and last name.
4. **Export database**: Exports the current database of policyholders to a CSV file.
5. **Exit**: Terminates the program.

## Code Structure

- **`InsuredPerson`**: A class that defines the attributes of a policyholder such as first name, last name, age, and phone number.
- **`InsuranceAgent`**: Contains methods for adding records, displaying policyholders, searching, and exporting data.
- **`RecordData`**: Contains functions for processing user input and validating it, including normalizing phone numbers.

## License

This project was created as a test assignment and is intended for educational purposes.

## Contact

The project was created by Jean Kocman.
