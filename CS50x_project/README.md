<a href="README.md"><img src="https://em-content.zobj.net/thumbs/120/twitter/322/flag-united-kingdom_1f1ec-1f1e7.png" alt="English" width="30"/></a>
<a href="README.cs.md"><img src="https://em-content.zobj.net/thumbs/120/twitter/322/flag-czechia_1f1e8-1f1ff.png" alt="Čeština" width="30"/></a>
# Ludo Game

#### Video Demo: [LUDO Game video](https://youtu.be/VCyraBtktCQ)


#### Description:
The **Ludo Game** is an interactive web-based version of the beloved board game, developed as my CS50x final project. This application combines modern web development techniques using HTML, CSS, and JavaScript for the frontend, and Python with Flask for the backend. It showcases a cohesive digital recreation of Ludo, emphasizing robust functionality and user engagement.

## Project Overview

The game replicates the core mechanics of Ludo, allowing multiple players to engage in strategic play. The application is designed to simulate real-world gameplay dynamics like dice rolling, piece movement, and automated turn management, all within an intuitive and visually pleasing interface.

### Core Features

- **Responsive User Interface**: Styled with Bootstrap to ensure the layout is adaptable across devices and screen sizes.
- **Interactive Gameplay**: Automated logic for piece movement and strategic game decisions based on dice outcomes.
- **Dynamic UI Components**: Features like animated pieces and player status indicators enhance the interactive experience.

## File Structure
### app.py

This Python file is the centerpiece of the project, running the Flask server to handle web requests. Flask acts as a lightweight yet powerful framework for integrating back-end functionality with the front-end interface, providing an optimal setup for full-stack web development.

### templates/index.html

Defines the structural layout of the game using HTML. As the interface template, it sets the stage for the board design, player status, and integrates external styles and scripts for functionality.

### static/styles.css

Contains the styling rules that define the aesthetics of the game. Leveraging CSS alongside Bootstrap, it brings forth a responsive and visually distinct game environment with clear differentiation for player pieces and board status.

### static/script.js

Holds the JavaScript logic central to game mechanics and interactivity. Functions manage game flow, such as piece movements, player turn transitions, and animations, ensuring seamless gameplay.

## Design Choices

Several thoughtful design decisions underpin this project:

- **Backend Integration with Flask**: Chosen for its simplicity and scalability, Flask facilitates easy expansion of the application, such as future database connectivity for game state saving.
- **Full-Stack Development**: Using Python and Flask provides capabilities beyond what HTML, CSS, and JavaScript alone can achieve. This enables server-side computing, easier management of application states, and smooth integration of databases (e.g., SQL for saving game progress), laying a foundation for advanced features.
- **Game Logic Automation**: Implementing automatic moves for pieces when they reach strategic play positions reflects a focus on enhancing user experience and usability.

## Future Development

A significant area for future work is implementing persistent game state saving using an SQL database. This will enable features such as:
- **Game State Persistence**: Allow players to resume games at a later time.
- **Player Statistics**: Track and display historical data for games played, enhancing engagement via leaderboards and performance analytics.
- **Gameplay Optimization**: Given the current state of the code, there is still work to be done in the area of final debugging and code optimization.
    - **What is _working_**:
        - Creation of the game board - the game board is properly created, including the game path, pieces, and fields dedicated for these pieces, with a colored background.
        - Dice roll - rolling of random numbers between 1 and 6.
        - Game mechanism - basic Ludo game rules are applied, including three rolls for placing a piece onto the starting position, conditioned by rolling number 6.
        - Placing pieces - pieces are placed onto starting positions given for their colors.
        - Movement - pieces are moving on the game path from starting to safe positions.
        - Knock-off function - collision between different colors is handled properly and the knocked-off piece is transferred back to its initial position so it can be placed again onto the starting position according to standard Ludo game rules.
        - Animation - movement on the game path and knock-off functions are animated to be more visually appealing for users.
        - UI - basic information for the player like rolled number, buttons for interaction with the game are properly introduced. Tooltips for pieces are shown so the player knows what piece can be selected.
    - **What is _not working_**:
        - Advanced game logic - when it comes to slightly more complicated logic around proper acknowledgment of bonus roll, this sometimes is not working as intended.
        - Change of active piece - in some cases, when the user selects a piece standing in the initial position while another piece is on the game path, the game allows the player to roll three times (as the active piece is standing in the initial position), while it should recognize another piece is eligible for movement without the necessity to roll three times.
        - Pass turn - in some situations, the turn is passed not to the second player, but to the third. So, if the first player passes the turn, the second player is skipped.

### Benefits of Using Python and Flask

- **Ease of Integration**: Flask simplifies the integration of additional services like databases (MySQL or SQLite) to save and manage game states.
- **Scalable Architecture**: As gameplay features expand, Flask's scalability allows for more complex server-side operations without sacrificing performance.
- **Rich Libraries and Extensions**: Python's extensive ecosystem supports various needs from data handling to API development, enhancing the evolution of gaming projects.
- **Security and Efficiency**: Flask provides tools to secure the application efficiently, ensuring trusted data transactions and user interactions.

## Development Process

The project was developed through iterative cycles, where features were prototyped, tested, and refined. This approach supported a robust understanding of web development concepts while enhancing problem-solving abilities across the tech stack. During this process, AI-based tools such as CS50 Duck Debugger, Microsoft Copilot, and ChatGPT-4o mini were employed for debugging and optimizing complex sections of code. These tools significantly amplified productivity, especially when tackling challenging problems that required an outside perspective. CS50 Duck Debugger was particularly helpful in suggesting directions that might be useful while encouraging independent study—a great approach. Meanwhile, Microsoft Copilot and ChatGPT-4o mini provided valuable assistance in identifying bugs and explaining errors. They were very useful for understanding console.log messages, which were not always completely clear.

Microsoft Copilot also contributed to overall refactoring in the final phase of the code, as in the last couple of months, the code became very long.

It is worth saying that using only AI tools can be very confusing. You have to have a certain knowledge of coding in order to keep suggestions you are receiving in expected borders. Relying only on AI tools does not guarantee success.

## Conclusion

The Ludo Game project embodies a successful blend of design, logic, and interactive play. It represents significant learning and achievement in web development as part of the CS50x curriculum. Future developments will continue to enhance this foundation, expanding functionalities to provide even richer user experiences.

## Acknowledgments

Thanks to the CS50x team for their excellent curriculum and support through very well-prepared online lectures, shorts, and section videos. Additional gratitude to open-source communities for resources and tools like Flask and Bootstrap, which were used in the development of this project. Special thanks to CS50 Duck Debugger, ChatGPT-4o mini, and Microsoft Copilot for aiding in debugging and code optimization, which contributed significantly to the project's robustness and understanding of the coding process.
