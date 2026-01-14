document.addEventListener('DOMContentLoaded', () => {
    // Handle "Return to CLI" button
    const returnToCLIBtn = document.getElementById('returnToCLIBtn');
    if (returnToCLIBtn) {
        returnToCLIBtn.addEventListener('click', () => {
            // Show a message to the user
            const message = `
╔════════════════════════════════════════════╗
║  Information about CLI Mode                ║
╚════════════════════════════════════════════╝

About CLI Mode:
- CLI mode is only available when running locally
- Use: python project.py

Current Mode:
- You are running in WEB MODE on Render.com
- This is optimized for browser access
- All features are available in this interface

To use CLI mode:
1. Run the application locally with: python project.py
2. Select option 7 from the menu to switch to web
3. Or use options 1-6 for CLI operations

Thank you for using Headache Tracker!
            `;
            alert(message);
        });
    }
    
    // Initial setup: Fetch records and update table & chart when the page loads
    fetchRecordsAndUpdate();

    // Fetch headache data segmented by trigger and initialize the graph
    fetch('/headaches_by_trigger')
        .then(response => response.json())
        .then(data => {
            updateTriggerGraph(data);
        });

    // Event listener for the headache record submission form
    document.getElementById('headacheForm').addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the form from submitting via the browser's default method

        // Collect data from the form inputs
        const formData = {
            user_name: document.getElementById('userName').value.trim(),
            user_age: document.getElementById('userAge').value,
            user_sex: document.getElementById('userSex').value,
            date_of_headache: document.getElementById('headacheDate').value,
            time_of_headache: document.getElementById('headacheTime').value,
            duration: document.getElementById('duration').value,
            intensity: document.getElementById('intensity').value,
            trigger: document.getElementById('trigger').value,
            headache_type: document.getElementById('headacheType').value,
            stress_level: document.getElementById('stressLevel').value,
            sleep_quality: document.getElementById('sleepQuality').value,
            medication: document.getElementById('medication').value,
            dosage: document.getElementById('dosage').value,
            effectiveness: document.getElementById('effectiveness').value
        };

        try {
            // Send form data to the server, expecting a JSON response
            const response = await fetch('/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });
            const result = await response.json();

            // Alert the user with a message from the server response
            alert(result.message || result.error);

            // Reset the form upon successful submission
            document.getElementById('headacheForm').reset();

            // Fetch updated records and refresh table and chart
            fetchRecordsAndUpdate();

            // Fetch the latest data for the graph and update it
            fetch('/headaches_by_trigger')
                .then(response => response.json())
                .then(data => {
                    // Call the function to update the graph with new data
                    updateTriggerGraph(data);
                });

        } catch (error) {
            console.error('Error adding record:', error);
            alert('An error occurred while adding the record. Please try again.');
        }
    });

    // Function to fetch records from the server and update table and charts
    async function fetchRecordsAndUpdate() {
        try {
            const response = await fetch('/records');
            const data = await response.json();

            // Generate HTML for the table and update the table's inner HTML
            const tableHTML = generateTableHTML(data.records, data.columns);
            document.getElementById('recordTable').innerHTML = tableHTML;

            // Update the general graphs with new data
            updateGraph(data.records);
        } catch (error) {
            console.error('Error fetching records:', error);
        }
    }

    // Function to generate HTML for the table
    function generateTableHTML(records, columns) {
        let html = '<thead><tr>';

        // Append columns to the table header
        columns.forEach(column => html += `<th>${column}</th>`);
        html += '</tr></thead><tbody>';

        // Append each record as a row in the table
        records.forEach(record => {
            html += '<tr>';
            record.forEach(field => html += `<td>${field}</td>`);
            html += '</tr>';
        });

        html += '</tbody>';
        return html;
    }

    // Function to generate an array of random RGBA colors
    function generateRandomColors(numColors) {
        const colors = [];
        for (let i = 0; i < numColors; i++) {
            // Create random color for each iteration
            const color = `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.2)`;
            colors.push(color);
        }
        return colors;
    }

    // Function to update the trigger graph with provided records
    function updateTriggerGraph(records) {
        const ctx = document.getElementById('myTriggerChart').getContext('2d');

        // Extract labels (triggers) and data (headache counts) for the graph
        const labels = records.map(record => record.trigger);
        const data = records.map(record => record.headache_count);

        // Generate background and border colors for the graph segments
        const backgroundColor = generateRandomColors(labels.length);
        const borderColor = backgroundColor.map(color => color.replace('0.2', '1'));

        // Create a new pie chart using Chart.js
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: '# of Headaches per Diet Trigger',
                    data: data,
                    backgroundColor: backgroundColor,
                    borderColor: borderColor,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Headaches by Diet Trigger'
                    }
                }
            }
        });
    }
});
