/* template/script.js */

let players = ['red', 'blue', 'yellow', 'green'];
let currentPlayerIndex = 0; // Start with the first player
let rolls = {
    red: 0,
    blue: 0,
    green: 0,
    yellow: 0
}; // Track rolls for each player
let currentPlayer = players[currentPlayerIndex]; // Current player
let diceRoll; // Declare diceRoll with let to limit scope
let currentRolls = 0; // Initialize currentRolls at the top
let selectedPieceNumber = null; // Move this declaration closer to its usage
let isGameOver = false;

class Piece {
    constructor(color, position) {
        this.color = color;
        this.position = position;
        this.hasStarted = false;
    }
}
// Creates a game with given parameters
const BOARD_SIZE = 11;
const NUM_PIECES = 4;
const COLORS = ['red', 'blue', 'green', 'yellow'];
const board = Array.from({
    length: BOARD_SIZE
}, () => Array(BOARD_SIZE).fill(null));
const pieces = {};
COLORS.forEach(color => {
    pieces[color] = Array.from({
        length: NUM_PIECES
    }, () => new Piece(color, 0));
});

const startingPositions = {
    red: {
        column: 0,
        row: 4
    },
    blue: {
        column: 6,
        row: 0
    },
    green: {
        column: 4,
        row: 10
    },
    yellow: {
        column: 10,
        row: 6
    }
};

const startingPathPositions = {
    red: null,
    blue: null,
    green: null,
    yellow: null
};

const initialPositions = {
    red: [{
        column: 0,
        row: 0
    }, {
        column: 1,
        row: 0
    }, {
        column: 0,
        row: 1
    }, {
        column: 1,
        row: 1
    }],
    blue: [{
        column: 9,
        row: 0
    }, {
        column: 10,
        row: 0
    }, {
        column: 9,
        row: 1
    }, {
        column: 10,
        row: 1
    }],
    green: [{
        column: 0,
        row: 9
    }, {
        column: 1,
        row: 9
    }, {
        column: 0,
        row: 10
    }, {
        column: 1,
        row: 10
    }],
    yellow: [{
        column: 10,
        row: 10
    }, {
        column: 9,
        row: 10
    }, {
        column: 10,
        row: 9
    }, {
        column: 9,
        row: 9
    }]
};

const safePositions = {
    red: [{
        column: 1,
        row: 5
    }, {
        column: 2,
        row: 5
    }, {
        column: 3,
        row: 5
    }, {
        column: 4,
        row: 5
    }],
    blue: [{
        column: 5,
        row: 1
    }, {
        column: 5,
        row: 2
    }, {
        column: 5,
        row: 3
    }, {
        column: 5,
        row: 4
    }],
    green: [{
        column: 5,
        row: 9
    }, {
        column: 5,
        row: 8
    }, {
        column: 5,
        row: 7
    }, {
        column: 5,
        row: 6
    }],
    yellow: [{
        column: 9,
        row: 5
    }, {
        column: 8,
        row: 5
    }, {
        column: 7,
        row: 5
    }, {
        column: 6,
        row: 5
    }]
};
const path = [
    // path on which pieces can move on //
    {
        column: 0,
        row: 4
    }, {
        column: 1,
        row: 4
    }, {
        column: 2,
        row: 4
    }, {
        column: 3,
        row: 4
    }, {
        column: 4,
        row: 4
    },
    {
        column: 4,
        row: 3
    }, {
        column: 4,
        row: 2
    }, {
        column: 4,
        row: 1
    }, {
        column: 4,
        row: 0
    },
    {
        column: 5,
        row: 0
    },
    {
        column: 6,
        row: 0
    }, {
        column: 6,
        row: 1
    }, {
        column: 6,
        row: 2
    }, {
        column: 6,
        row: 3
    }, {
        column: 6,
        row: 4
    },
    {
        column: 7,
        row: 4
    }, {
        column: 8,
        row: 4
    }, {
        column: 9,
        row: 4
    }, {
        column: 10,
        row: 4
    },
    {
        column: 10,
        row: 5
    },
    {
        column: 10,
        row: 6
    }, {
        column: 9,
        row: 6
    }, {
        column: 8,
        row: 6
    }, {
        column: 7,
        row: 6
    }, {
        column: 6,
        row: 6
    },
    {
        column: 6,
        row: 7
    }, {
        column: 6,
        row: 8
    }, {
        column: 6,
        row: 9
    }, {
        column: 6,
        row: 10
    },
    {
        column: 5,
        row: 10
    },
    {
        column: 4,
        row: 10
    }, {
        column: 4,
        row: 9
    }, {
        column: 4,
        row: 8
    }, {
        column: 4,
        row: 7
    }, {
        column: 4,
        row: 6
    },
    {
        column: 3,
        row: 6
    }, {
        column: 2,
        row: 6
    }, {
        column: 1,
        row: 6
    }, {
        column: 0,
        row: 6
    },
    {
        column: 0,
        row: 5
    },
];

function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

// Rotates path so each piece color has same length of path
function rotatePath(path, startPosition) {
    const startIndex = path.findIndex(p => p.column === startPosition.column && p.row === startPosition.row);
    return [...path.slice(startIndex), ...path.slice(0, startIndex)];
}

// Creates a new constant named paths (not path but paths). These are paths given for each colour with its starting positions
// and also with safe positions.
const paths = {
    red: [...rotatePath(path, startingPositions.red), ...safePositions.red],
    blue: [...rotatePath(path, startingPositions.blue), ...safePositions.blue],
    green: [...rotatePath(path, startingPositions.green), ...safePositions.green],
    yellow: [...rotatePath(path, startingPositions.yellow), ...safePositions.yellow]
};

function calculateStartingPathPositions() {
    startingPathPositions.red = getPathIndex(startingPositions.red, 'red') + 1;
    console.log(`Starting path position for red: ${startingPathPositions.red}`);
    startingPathPositions.blue = getPathIndex(startingPositions.blue, 'blue') + 1;
    console.log(`Starting path position for blue: ${startingPathPositions.blue}`);
    startingPathPositions.green = getPathIndex(startingPositions.green, 'green') + 1;
    console.log(`Starting path position for green: ${startingPathPositions.green}`);
    startingPathPositions.yellow = getPathIndex(startingPositions.yellow, 'yellow') + 1;
    console.log(`Starting path position for yellow: ${startingPathPositions.yellow}`);
}

const cellClasses = {
    red: 'red-cell',
    blue: 'blue-cell',
    green: 'green-cell',
    yellow: 'yellow-cell'
};

let currentPieceNumber = {
    red: 1,
    blue: 1,
    green: 1,
    yellow: 1
};

// Creates a game board
function createBoard() {
    const boardElement = document.getElementById('board');
    for (let i = 0; i < BOARD_SIZE; i++) {
        for (let j = 0; j < BOARD_SIZE; j++) {
            const cell = document.createElement('div');
            cell.id = `cell-${i}-${j}`;
            cell.style.gridColumnStart = i + 1;
            cell.style.gridRowStart = j + 1;

            // Check if the cell (field) is part of the path, initial, or safe positions
            if (path.some(pos => pos.column === i && pos.row === j) ||
                Object.values(initialPositions).flat().some(pos => pos.column === i && pos.row === j) ||
                Object.values(safePositions).flat().some(pos => pos.column === i && pos.row === j)) {
                cell.classList.add('path-cell');
            }

            boardElement.appendChild(cell);
        }
    }
}

// Creates starting arrows showing direction of movement on the game board
function addStartarrows() {
    const boardElement = document.getElementById('board');

    for (let color in startingPositions) {
        const position = startingPositions[color];
        const arrowIcon = document.createElement('i');
        // Set the icon class based on the color
        switch (color) {
            case 'red':
                arrowIcon.classList.add('bi', 'bi-arrow-right-circle', `${color}-start`); // Red points right
                break;
            case 'blue':
                arrowIcon.classList.add('bi', 'bi-arrow-down-circle', `${color}-start`); // Blue points down
                break;
            case 'green':
                arrowIcon.classList.add('bi', 'bi-arrow-up-circle', `${color}-start`); // Green points up
                break;
            case 'yellow':
                arrowIcon.classList.add('bi', 'bi-arrow-left-circle', `${color}-start`); // Yellow points left
                break;
        }

        arrowIcon.style.fontSize = '2.1rem'; // Set the size of the arrow icon
        arrowIcon.style.position = 'absolute'; // Position it absolutely

        // Calculate the position in pixels based on the grid layout
        const columnStart = position.column * 50; // Assuming each cell is 50px wide
        const rowStart = position.row * 50; // Assuming each cell is 50px tall

        // Set the left and top positions and center the icon
        arrowIcon.style.left = `${columnStart}px`;
        arrowIcon.style.top = `${rowStart}px`;
        arrowIcon.style.width = '50px';
        arrowIcon.style.height = '50px';
        arrowIcon.style.display = 'flex';
        arrowIcon.style.alignItems = 'center';
        arrowIcon.style.justifyContent = 'center';

        // Append the arrow icon to the board
        boardElement.appendChild(arrowIcon);
    }
}

// Defining of safe - finish - positions.
function setSafePositions() {
    for (let color in safePositions) {
        safePositions[color].forEach(position => {
            const cell = document.getElementById(`cell-${position.column}-${position.row}`);
            if (cell) {
                cell.classList.add(cellClasses[color]); // Add the color class to the cell
            } else {
                console.error(`Cell not found: cell-${position.column}-${position.row}`);
            }
        });
    }
    console.log("Safe positions set:", safePositions);
}

// Sets only visual position, UI, not a position in data structure (position not positions defined above)
function setPosition(pieceId, position) {
    if (!position) {
        console.error(`Invalid position for pieceId: ${pieceId}, received position:`, position);
        return;
    }
    const pieceElement = document.getElementById(pieceId);
    console.log(`Setting position for ${pieceId} to column: ${position.column}, row: ${position.row}`);
    pieceElement.style.gridColumnStart = position.column + 1;
    pieceElement.style.gridRowStart = position.row + 1;
}

// Sets initial positions for each piece. This is waiting zone from which pieces are place on starting position.
function setInitialPositions() {
    console.log("Setting initial positions");
    for (let color in pieces) {
        pieces[color].forEach((piece, index) => {
            const pieceElement = document.createElement('div');
            pieceElement.id = `${color}Piece${index + 1}`;
            pieceElement.classList.add('piece', `${color}-piece`);

            // Add a title attribute to show the piece number and color
            pieceElement.title = `${capitalize(color)} Piece ${index + 1}`;

            const innerCircle = document.createElement('div');
            innerCircle.classList.add('inner-circle');
            pieceElement.appendChild(innerCircle);
            document.getElementById('board').appendChild(pieceElement);
            console.log(`Placing ${pieceElement.id} at initial position:`, initialPositions[color][index]);
            setPosition(pieceElement.id, initialPositions[color][index]);

            // Set the background color of the cell where the piece is placed
            const cell = document.getElementById(`cell-${initialPositions[color][index].column}-${initialPositions[color][index].row}`);
            if (cell) {
                cell.classList.remove(...Object.values(cellClasses)); // Remove any existing color classes - to be sure no conflict with other settings happends
                cell.classList.add(cellClasses[color]); // Add the correct color class to the cell
            } else {
                console.error(`Cell not found: cell-${initialPositions[color][index].column}-${initialPositions[color][index].row}`);
            }
        });
    }
}

// Basic function for rolling the dice - generating random number in a given range
function rollDice() {
    return Math.floor(Math.random() * 6) + 1; // Return a random roll between 1 and 6
}
let color = players[currentPlayerIndex]; // Get the current player's color
const nextPieceNumber = findNextEligiblePiece(color);
if (nextPieceNumber !== null) {
    movePiece(color, nextPieceNumber, diceRoll);
} else {
    console.log(`No eligible pieces for ${color}. Ending turn.`);
    endTurn();
}
// This function should find the index of a given position (with column and row) in the path array.
function getPathIndex(position, color) {
    if (paths && paths[color]) {
        const index = paths[color].findIndex(p => p.column === position.column && p.row === position.row);
        if (index === -1) {
            console.error(`Position not found in path for color: ${color}`);
            return -1;
        }
        console.log(`getPathIndex for position (${position.column}, ${position.row}): ${index + 1}`);
        return index + 1;
    } else {
        console.error(`Path not found for color: ${color}`);
        return -1;
    }
}

// Working with results of rollDice function. This logic was consulted with AI tools mentioned in README.md file.
function handleDiceRoll() {
    console.log("Dice roll triggered for current player:", currentPlayer);

    // Validate player colors
    if (!ensureValidPlayerColor(currentPlayer)) {
        console.error('Unexpected currentPlayer value: ', currentPlayer);
        return;
    }

    // Determine if any pieces are in play or can start movement
    const hasPiecesOnPath = pieces[currentPlayer].some(piece => piece.position > 0 && piece.position < paths[currentPlayer].length);
    const hasPiecesInInitial = pieces[currentPlayer].some(piece => piece.position === 0);

    // Perform dice roll - as no errors mentioned above were discovered
    diceRoll = rollDice();
    console.log(`Dice Roll for ${currentPlayer}: ${diceRoll}`);

    // Ensure current player is valid and has pieces to play with - checking player availibility
    if (typeof currentPlayer === 'undefined' || !pieces[currentPlayer]) {
        console.error(`Unexpected currentPlayer value: ${currentPlayer}`);
        return;
    }
    // UI message with result of diceRoll
    document.getElementById('diceResult').innerText = `${capitalize(currentPlayer)} rolled: ${diceRoll}`;

    currentRolls++;
    rolls[currentPlayer]++;

    const currentPieceIndex = currentPieceNumber[currentPlayer] - 1;

    if (currentPieceIndex < 0 || currentPieceIndex >= pieces[currentPlayer].length) {
        console.error(`Invalid current piece number: ${currentPieceNumber[currentPlayer]}`);
        return;
    }

    const currentPiece = pieces[currentPlayer][currentPieceIndex];

    if (!currentPiece) {
        console.error(`Piece not found for current player: ${currentPlayer}, piece number: ${currentPieceIndex + 1}`);
        return;
    }

    // Check if the player can move or needs to make a choice
    const tryingToMove = diceRoll === 6 || currentPiece.hasStarted;

    if (diceRoll === 6) {
        if (hasPiecesOnPath && hasPiecesInInitial) {
            // When both starting a new piece and moving one are options
            promptPlayerChoice();
            return;
        } else if (hasPiecesInInitial) {
            // Automatically start if no pieces are on the path - places piece from initialPosition to startingPosition
            console.log("Automatically starting a new piece.");
            const pieceNumber = pieces[currentPlayer].findIndex(piece => !piece.hasStarted) + 1;
            if (pieceNumber) {
                movePiece(currentPlayer, pieceNumber, 6);
            }
            handleBonusRoll();
            return;
        }
    }

    if (tryingToMove) {
        movePiece(currentPlayer, currentPieceNumber[currentPlayer], diceRoll);
    } else {
        console.log(`No eligible pieces to move for ${currentPlayer}`);
    }

    // Check whether a bonus roll - aditional roll - is recognised to the player
    const allowReroll = (hasPiecesInInitial && currentRolls < 3) || (!hasPiecesInInitial && hasPiecesOnPath && currentRolls < 1);
    if (allowReroll) {
        console.log(`Roll ${currentRolls} of 3. Allowing another roll.`);
        return;
    }

    // End the turn when no further rolls or choices are possible
    endTurn();
}

// Function which is ending all actions for given player as per stated conditions
function endTurn() {
    console.log("Ending turn for player:", currentPlayer);

    // Disable the dice roll button and reset current rolls
    document.getElementById('rollDice').disabled = true;
    currentRolls = 0; // Reset for the next player

    // Check for a win condition every time a player's turn ends
    checkWinCondition();

    // If no winner is found (i.e., the game is not over), proceed to the next player
    if (!isGameOver) {
        nextPlayer();
    }
}

// Slow animated movement of pieces on the board
function movePieceSmoothly(pieceId, startIndex, endIndex, path, callback) {
    let currentIndex = startIndex;
    const pieceElement = document.getElementById(pieceId);
    pieceElement.classList.add('animate-move-start');

    function moveStep() {
        if (currentIndex < endIndex) {
            currentIndex++;
            console.log(`Moving ${pieceId} to position:`, path[currentIndex]);
            setPosition(pieceId, path[currentIndex]);
            setTimeout(moveStep, 450); // Adjust the delay as needed
        } else {
            setTimeout(() => {
                pieceElement.classList.remove('animate-move-start');
                pieceElement.classList.add('animate-move-end');
                setTimeout(() => {
                    pieceElement.classList.remove('animate-move-end');
                    if (callback) callback(); // Call the callback function (handleCollision)
                }, 500); // Match the duration of the end animation
            }, 50); // Short delay before adding the end animation - so it is recognisable
        }
    }

    moveStep();
}

// function addMoveAnimation(pieceId) {
//     const pieceElement = document.getElementById(pieceId);
//     pieceElement.classList.add('highlight-move');
//     setTimeout(() => pieceElement.classList.remove('highlight-move'), 500);
// }

// Checking whether piece can enter safe zone - check for free cells
function isSafePositionFree(position) {
    for (let color in pieces) {
        if (pieces[color].some(piece => {
                const piecePosition = paths[color][piece.position - 1]; // Convert index to actual position
                return piecePosition && piecePosition.column === position.column && piecePosition.row === position.row;
            })) {
            return false; // Position is occupied
        }
    }
    return true; // Position is free
}

// Is working as knock-off function which transers piece back to initial position in case of collisions
function movePieceToInitialPosition(piece, color) {
    const pieceId = `${color}Piece${pieces[color].indexOf(piece) + 1}`;
    const pieceElement = document.getElementById(pieceId);
    const initialPos = initialPositions[color][pieces[color].indexOf(piece)];

    // Add the kick-off animation class
    pieceElement.classList.add(`${color}-kick-off`);

    // Wait for the animation to complete before resetting the piece position
    setTimeout(() => {
        piece.position = 0;
        piece.hasStarted = false;
        piece.hasReset = false; // Mark the piece as reset. Originally was true, but was causing kicked-off pieces imune to next collisions
        setPosition(pieceId, initialPos); // Set the piece back to its initial position on the board
        pieceElement.classList.remove(`${color}-kick-off`); // Remove the animation class
        console.log(`${color} piece ${pieces[color].indexOf(piece) + 1} moved to initial position.`);
        console.log(`Updated piece position: ${piece.position}, hasStarted: ${piece.hasStarted}, hasReset: ${piece.hasReset}`);
    }, 500); // Match the duration of the animation
}

// Suggested by Microsoft Copilot. Not working as expected though but idea is interesting
// Logic for selection of active piece - to make it active for dice rolls
function handlePieceSelection(color, pieceNumber, diceRoll) {
    const piece = pieces[color][pieceNumber - 1];

    if (!piece.hasStarted && diceRoll !== 6) {
        console.log(`Piece ${pieceNumber} of ${color} hasn't started and dice roll is not 6.`);
        return promptForAnotherPiece(color, diceRoll);
    }

    if (isPieceInSafePosition(piece, color)) {
        console.log(`Piece ${pieceNumber} of ${color} is already in the safe zone and cannot move.`);
        return promptForAnotherPiece(color, diceRoll);

    }

    if (checkPotentialCollision(color, pieceNumber, diceRoll)) {
        console.log(`Collision detected! Select another piece, or pass the turn.`);
        return promptForAnotherPiece(color, diceRoll);
    }

    movePiece(color, pieceNumber, diceRoll);
}

// Checking collisions upfront the movement so player can take decision before piece will move
function checkPotentialCollision(color, pieceNumber, diceRoll) {
    const piece = pieces[color][pieceNumber - 1];
    const path = paths[color];
    let newPosition = piece.position + diceRoll;

    if (newPosition > path.length) {
        // Safe zone check logic (if applicable)
        return false;
    }

    const newPiecePosition = path[newPosition - 1];

    // Check for collision with the same color. Not working always good.
    for (let otherPiece of pieces[color]) {
        if (otherPiece !== piece && otherPiece.position !== 0) {
            const otherPosition = paths[color][otherPiece.position - 1];
            if (otherPosition && newPiecePosition &&
                otherPosition.column === newPiecePosition.column &&
                otherPosition.row === newPiecePosition.row) {
                console.log(`Collision within same color detected.`);
                return true;
            }
        }
    }

    // Check for collision with other colors as necessary
    return false;
}

// function checkPotentialCollision(color, pieceNumber, diceRoll) {
//     const piece = pieces[color][pieceNumber - 1];
//     const path = paths[color];
//     const newPosition = piece.position + diceRoll - 1;
//     const newPiecePosition = path[newPosition];

//     // Check for collisions with same and different colors
//     for (const otherColor of COLORS) {
//         for (const otherPiece of pieces[otherColor]) {
//             if (otherPiece !== piece && otherPiece.position !== 0) {
//                 const pos = paths[otherColor][otherPiece.position - 1];
//                 if (pos && newPiecePosition && pos.column === newPiecePosition.column && pos.row === newPiecePosition.row) {
//                     console.log(`Collision detected for piece ${pieceNumber} of ${color}.`);
//                     return true;
//                 }
//             }
//         }
//     }
//     return false;
// }


// Is handling collisions after pre-collision check is done
function handleCollision(piece) {
    if (!piece || piece.position === 0) return; // Ignore undefined pieces or those at initial positions

    const currentPiecePath = paths[piece.color][piece.position - 1];
    console.log(`Checking collision for piece: ${piece.color} at position: ${piece.position}`);

    // Check for collisions within the same color
    for (let i = 0; i < pieces[piece.color].length; i++) {
        const otherPiece = pieces[piece.color][i];
        if (otherPiece !== piece && otherPiece.position !== 0) {
            const otherPiecePath = paths[piece.color][otherPiece.position - 1];
            if (otherPiecePath && otherPiecePath.column === currentPiecePath.column && otherPiecePath.row === currentPiecePath.row) {
                console.log(`Collision within same color: ${piece.color}`);
                showAlert(`Collision detected within the same color: ${piece.color}. You may need to adjust your move strategy.`);
                return promptForAnotherPiece(piece.color);
            }
        }
    }

    // Handle collisions with pieces of other colors
    COLORS.filter(c => c !== piece.color).forEach(otherColor => {
        pieces[otherColor].forEach(otherPiece => {
            if (otherPiece.position !== 0) {
                const otherPiecePath = paths[otherColor][otherPiece.position - 1];
                if (otherPiecePath && otherPiecePath.column === currentPiecePath.column && otherPiecePath.row === currentPiecePath.row) {
                    console.log(`Collision detected! Resetting ${otherColor} piece ${pieces[otherColor].indexOf(otherPiece) + 1} to initial position.`);
                    movePieceToInitialPosition(otherPiece, otherColor);
                }
            }
        });
    });
}

// Asking user to select alternative piece for further movement, or to pass turn.
function promptForAnotherPiece(color, diceRoll) {
    document.getElementById('rollDice').disabled = true;

    const initialPieces = pieces[color].filter(piece => !piece.hasStarted && piece.position === 0);
    const onBoardPieces = pieces[color].filter(piece => piece.hasStarted && !isPieceInSafePosition(piece, color));

    let eligiblePieces = [];

    if (initialPieces.length > 0 && diceRoll === 6) {
        eligiblePieces = initialPieces; // Prioritize new startable pieces for roll of 6
    } else if (onBoardPieces.length > 0) {
        eligiblePieces = onBoardPieces.filter(piece => !checkPotentialCollision(color, pieces[color].indexOf(piece) + 1, diceRoll));
    }

    const promptContainer = document.getElementById('prompt');
    promptContainer.innerHTML = '';
    promptContainer.style.display = 'block';

    if (eligiblePieces.length > 0) {
        const upperText = document.createElement('div');
        upperText.innerText = `Select a piece for ${capitalize(color)}, or pass the turn.`;
        promptContainer.appendChild(upperText);

        eligiblePieces.forEach(piece => {
            const index = pieces[color].indexOf(piece);
            const pieceButton = document.createElement('button');
            pieceButton.innerText = `Piece ${index + 1}`;
            pieceButton.classList.add('btn', 'btn-secondary', 'mb-2', 'me-2');
            pieceButton.addEventListener('click', () => {
                handlePieceSelection(color, index + 1, diceRoll);
                closePrompt(promptContainer);
            });
            promptContainer.appendChild(pieceButton);
        });

        const passButton = document.createElement('button');
        passButton.innerText = `Pass Turn`;
        passButton.classList.add('btn', 'btn-secondary', 'mb-2', 'me-2');
        passButton.addEventListener('click', () => {
            closePrompt(promptContainer);
            endTurn();
        });
        promptContainer.appendChild(passButton);
    } else {
        handlePassAutomatically(promptContainer);
    }
}

// Function to close the prompt and reset state - with refferece to function promptForAnotherPiece
function closePrompt(promptContainer) {
    promptContainer.innerHTML = '';
    promptContainer.style.display = 'none';
    document.getElementById('rollDice').disabled = false;
}

// New helper function for automatic passing - with refferece to function promptForAnotherPiece
function handlePassAutomatically(promptContainer) {
    const noMoveText = document.createElement('div');
    noMoveText.innerText = `No eligible pieces to move. Passing turn automatically.`;
    promptContainer.appendChild(noMoveText);

    setTimeout(() => {
        closePrompt(promptContainer);
        endTurn();
    }, 2000);
}

console.log(`Before movePiece: ${pieces[currentPlayer][currentPieceNumber[currentPlayer] - 1].hasStarted}`);

// Findins another piece capable to move, if an active one cannot move on
function findNextEligiblePiece(color) {
    if (!pieces[color]) {
        console.error(`No pieces found for color: ${color}`);
        return null;
    }
    for (let i = 0; i < pieces[color].length; i++) {
        const piece = pieces[color][i];
        if ((!piece.hasStarted && piece.position === 0) || (piece.hasStarted && piece.position > 0 && piece.position < paths[color].length)) {
            console.log(`Eligible piece for ${color}: ${i + 1}`);
            return i + 1;
        }
    }
    console.log(`No eligible pieces for ${color}`);
    return null;
}

function showAlert(message) {
    const alertBox = document.getElementById('alertBox');
    const alertMessage = document.getElementById('alertMessage');
    if (alertBox && alertMessage) {
        alertMessage.innerText = message;
        alertBox.style.display = 'block';
    } else {
        console.error("Alert box or message element not found.");
        alert("A critical UI component is missing. Please refresh the page.");
    }
}

function hideAlert() {
    const alertBox = document.getElementById('alertBox');
    if (alertBox) {
        alertBox.style.display = 'none';
    } else {
        console.error("Alert box element not found.");
    }
}
// Key function for whole game. Inputs form Duck Debuger were very helpful here.
function movePiece(color, pieceNumber, diceRoll) {
    const pieceId = `${color}Piece${pieceNumber}`;
    const piece = pieces[color][pieceNumber - 1];

    if (!piece || !paths[color]) {
        console.error(`Invalid setup or piece not found for color ${color} and piece number ${pieceNumber}`);
        return;
    }

    if (isPieceInSafePosition(piece, color)) {
        console.log(`Piece ${pieceNumber} of ${color} is already in the safe zone and cannot move further.`);
        return promptForAnotherPiece(color, diceRoll);
    }

    if (diceRoll === 6 && !piece.hasStarted) {
        piece.hasStarted = true;
        piece.position = 1;
        setPosition(pieceId, startingPositions[color]);
        console.log(`Dice 6 start for ${color} piece ${pieceNumber}`);
        setTimeout(() => handleCollision(piece), 500);
        checkWinCondition(); // Check here after every move
        return;
    }

    let newPosition = piece.position + diceRoll;

    if (isPotentialCollision(color, piece, newPosition)) {
        console.log(`Collision detected for ${color} piece ${pieceNumber} at newPosition: ${newPosition}`);
        return promptForAnotherPiece(color, diceRoll);
    }

    if (canEnterSafeZone(color, piece, newPosition)) {
        const safeIndex = newPosition - (paths[color].length - safePositions[color].length) - 1;
        if (safeIndex >= 0 && safeIndex < safePositions[color].length && isSafePositionFree(safePositions[color][safeIndex])) {
            piece.position = newPosition;
            movePieceSmoothly(pieceId, piece.position - diceRoll - 1, paths[color].length - safePositions[color].length + safeIndex, paths[color], () => {
                setPosition(pieceId, safePositions[color][safeIndex]);
                setTimeout(() => handleCollision(piece), 500);
            });

            checkWinCondition(); // Check here after every move

            if (diceRoll !== 6 && !isGameOver) {
                endTurn();
            } else if (!isGameOver) {
                handleBonusRoll();
            }
            return;
        }
    }

    if (newPosition > 0 && newPosition <= paths[color].length) {
        piece.position = newPosition;
        const startIndex = piece.position - diceRoll - 1;
        movePieceSmoothly(pieceId, startIndex, newPosition - 1, paths[color], () => {
            setTimeout(() => handleCollision(piece), 500);
        });

        checkWinCondition(); // Check here after every move

        if (diceRoll !== 6 && !isGameOver) {
            endTurn();
        } else if (!isGameOver) {
            handleBonusRoll();
        }
    } else {
        console.error(`Invalid new position: ${newPosition}`);
    }
}


// Selection of an active piece
function selectPiece(pieceNumber) {
    console.log(`Piece ${pieceNumber} selected`);
    pieces[currentPlayer].forEach((piece, index) => {
        const pieceElement = document.getElementById(`${currentPlayer}Piece${index + 1}`);
        if (pieceElement) { // Check if the element exists
            if (index + 1 === pieceNumber) {
                pieceElement.classList.add('selected');
            } else {
                pieceElement.classList.remove('selected');
            }
        }
    });
    selectedPieceNumber = pieceNumber;
    currentPieceNumber[currentPlayer] = pieceNumber;

    // Hide the alert when a piece is selected
    hideAlert();
}

// Asking player to do an action
function promptPlayerChoice() {
    const choiceContainer = document.getElementById('choiceContainer') || document.createElement('div');
    choiceContainer.id = 'choiceContainer';
    choiceContainer.classList.add('mb-2');
    choiceContainer.innerHTML = ''; // Clear existing choices

    const rollDiceButton = document.getElementById('rollDice');

    const createButton = (text, className, callback) => {
        const button = document.createElement('button');
        button.innerText = text;
        button.classList.add('btn', className, 'mr-2');
        button.addEventListener('click', callback);
        choiceContainer.appendChild(button);
    };

    createButton('Move Piece', 'btn-success', () => {
        const piecesOnBoard = pieces[currentPlayer].filter(piece => piece.hasStarted);
        let pieceToMove;

        if (piecesOnBoard.length === 1) {
            // If only one piece has started, move that one
            pieceToMove = pieces[currentPlayer].findIndex(piece => piece.hasStarted) + 1;
        } else {
            // If multiple pieces are ready, rely on previous selection
            pieceToMove = selectedPieceNumber || pieces[currentPlayer].findIndex(piece => piece.hasStarted) + 1;
        }

        if (pieceToMove) {
            selectPiece(pieceToMove);
            movePiece(currentPlayer, pieceToMove, diceRoll);
        } else {
            console.log('No piece selected for moving.');
        }

        cleanupChoiceContainer();
        handleBonusRoll(); // Handle reroll logic if a six was rolled
    });

    createButton('Place New Piece', 'btn-warning', () => {
        const pieceNumber = pieces[currentPlayer].findIndex(piece => !piece.hasStarted) + 1;

        if (pieceNumber) {
            selectPiece(pieceNumber);
            movePiece(currentPlayer, pieceNumber, 6); // Move directly if six allows a new piece
        } else {
            console.log('No new pieces to place.');
        }

        cleanupChoiceContainer();
        handleBonusRoll();
    });

    document.body.appendChild(choiceContainer);

    // Attach piece click handlers for selection
    pieces[currentPlayer].forEach((piece, index) => {
        const pieceElement = document.getElementById(`${currentPlayer}Piece${index + 1}`);
        if (pieceElement) {
            pieceElement.addEventListener('click', () => selectPiece(index + 1));
        }
    });

    rollDiceButton.style.display = 'none';
}

// This is cleaning after function promptPlayerChoice crated selection buttons
function cleanupChoiceContainer() {
    const choiceContainer = document.getElementById('choiceContainer');
    if (choiceContainer) choiceContainer.remove();
    document.getElementById('rollDice').style.display = 'block';
}


// Heavilly supported by Microsoft Copilot due to necesitty of refactoring. In later phase of coding, AI tools proved to be helfpul for maintaining order in my code.
function handleBonusRoll() {
    if (diceRoll === 6) {
        console.log(`${currentPlayer} rolled a 6.`);

        // Check for pieces that can move on the current path
        const canMoveFurther = pieces[currentPlayer].some(piece => {
            if (piece.hasStarted) {
                return true; // If any piece has started, a bonus roll is warranted
            }
            const newPosition = piece.position + diceRoll;
            return !isPieceInSafePosition(piece, currentPlayer) &&
                !checkPotentialCollision(currentPlayer, pieces[currentPlayer].indexOf(piece) + 1, diceRoll) &&
                canEnterSafeZone(currentPlayer, piece, newPosition);
        });

        if (canMoveFurther) {
            console.log("Rolled a 6, allowing for a bonus roll.");
            setImmediateBonusRoll();
            return;
        }

        // Manage potential new starts from initial positions only if no moves are further possible
        const piecesInInitial = pieces[currentPlayer].filter(piece => !piece.hasStarted);
        if (piecesInInitial.length > 0) {
            const pieceToStartIndex = pieces[currentPlayer].findIndex(piece => !piece.hasStarted);
            if (pieceToStartIndex !== -1) {
                console.log(`Automatically starting piece ${pieceToStartIndex + 1} from initial position.`);
                selectPiece(pieceToStartIndex + 1);
                movePiece(currentPlayer, pieceToStartIndex + 1, 6);
                setImmediateBonusRoll(); // Ensure a bonus roll as new piece starts
                return;
            }
        }

        console.log("No pieces eligible to move after processing roll conditions.");
    }

    console.log("Ending turn, no bonus roll applies.");
    endTurn();
}

// Automatic bonuss roll in case no other choice is available
function setImmediateBonusRoll() {
    document.getElementById('currentPlayer').innerText = `${capitalize(currentPlayer)} gets another roll, because a 6 was rolled! Roll again!`;
    document.getElementById('rollDice').disabled = false; // Re-enable rolling when a 6 was rolled
}

// Checking whether safe some piece(s) is(are) in safe position
// function isPieceInSafePosition(piece, color) {
//     return !piece.hasStarted && safePositions[color].some(pos => pos.column === paths[color][piece.position - 1].column && pos.row === paths[color][piece.position - 1].row);
// }

// Checking whether piece of given color is alowed to safe position for given color
function canEnterSafeZone(color, piece, newPosition) {
    const pathLengthWithoutSafe = paths[color].length - safePositions[color].length;
    return newPosition > pathLengthWithoutSafe && newPosition <= paths[color].length;
}

// Function to handle the player's turn
function playerTurn() {
    if (!ensureValidPlayerColor(currentPlayer)) {
        console.error('Invalid current player detected at the start of playerTurn:', currentPlayer);
        return; // Exit if currentPlayer is invalid
    }
    let color = players[currentPlayerIndex]; // Get the current player's color

    console.log(`Setting up turn for player: ${currentPlayer}`);

    // Enable the roll dice button at the start of the player's turn
    document.getElementById('rollDice').disabled = false;
    currentRolls = 0; // Reset the current rolls
    rolls[currentPlayer] = 0; // Reset rolls for the current player

    // Check if any of the pieces are in the initial position
    const hasPiecesInInitial = pieces[currentPlayer].some(piece => piece.position === 0);
    const allPiecesNotOnPath = pieces[currentPlayer].every(
        piece => piece.position === 0 || isPieceInSafePosition(piece, currentPlayer)
    );

    if (hasPiecesInInitial && allPiecesNotOnPath) {
        document.getElementById('currentPlayer').innerText = capitalize(`${currentPlayer} can roll 3 times!`);
        currentRollsAllowed = 3;
    } else {
        document.getElementById('currentPlayer').innerText = capitalize(`${currentPlayer} can roll once.`);
        currentRollsAllowed = 1;
    }

    // Attach the handleDiceRoll event listener - is adding and removing as per game state
    document.getElementById('rollDice').removeEventListener('click', handleDiceRoll);
    document.getElementById('rollDice').addEventListener('click', handleDiceRoll);
}

function isPotentialCollision(color, piece, newPosition) {
    return pieces[color].some(otherPiece =>
        otherPiece !== piece && otherPiece.position === newPosition
    );
}

// Checking whether safe some piece(s) is(are) in safe position
function isPieceInSafePosition(piece, color) {
    if (!piece || typeof color !== 'string' || !COLORS.includes(color)) {
        console.error('Invalid piece or color for isPieceInSafePosition');
        return false;
    }
    if (!safePositions[color]) {
        console.error(`Safe positions not found for color: ${color}`);
        return false;
    }
    if (!piece.hasStarted) {
        return false;
    }

    const pathLengthWithoutSafe = paths[color].length - safePositions[color].length;
    if (piece.position <= pathLengthWithoutSafe) {
        return false; // The piece is not yet in the safe zone part of the path
    }

    const safeIndex = piece.position - pathLengthWithoutSafe - 1;
    return safeIndex >= 0 && safeIndex < safePositions[color].length;
}


// Suggested by AI. Idea came when console.log showed errors linked to unknown colors of pieces.
function ensureValidPlayerColor(player) {
    if (typeof player !== 'string' || !COLORS.includes(player)) {
        console.error('Invalid player color:', player);
        return false;
    }
    return true;
}

// Next player function
function nextPlayer() {
    let color = players[currentPlayerIndex]; // Get the current player's color
    currentPlayerIndex = (currentPlayerIndex + 1) % players.length;
    currentPlayer = players[currentPlayerIndex];
    console.log(`Now it's ${currentPlayer}'s turn`);
    document.getElementById('nextPlayer').innerText = `Now it's ${capitalize(currentPlayer)}'s turn`; // Display update for UI
    playerTurn(); // Prepare the next player's turn
}

// Function which si checking whether four pices of any colour are finally in safePosition - finish
function checkWinCondition() {
    if (isGameOver) return; // Prevent further checks if game is already over

    COLORS.forEach(color => {
        const allInSafePositions = pieces[color].every(piece => {
            // Check if the piece position is within safe range
            const pathIndex = piece.position;
            if (pathIndex <= 0 || pathIndex > paths[color].length) {
                return false; // Explicitly handle invalid index range
            }

            // Ensure the piece is at one of the safe end positions
            return safePositions[color].some(safePos =>
                safePos.column === paths[color][pathIndex - 1].column &&
                safePos.row === paths[color][pathIndex - 1].row
            );
        });

        if (allInSafePositions) {
            announceAndEndGame(color);
            isGameOver = true; // Set flag to stop further actions
            return; // Exit once a winner is found
        }
    });
}

// Annoucement of end of the game
function announceAndEndGame(winnerColor) {
    showWinMessage(winnerColor);

    // Optional: Hide or disable game controls
    document.getElementById('rollDice').style.display = 'none';
    const nextPlayerElement = document.getElementById('nextPlayer');
    if (nextPlayerElement) {
        nextPlayerElement.style.display = 'none'; // Optionally hide it
    }
}

function showWinMessage(color) {
    const currentPlayerDiv = document.getElementById('currentPlayer');
    currentPlayerDiv.textContent = `Congratulations, ${capitalize(color)} wins the game!`;
    currentPlayerDiv.classList.add('alert', 'alert-success'); // Add winning style
}

// Event listeners for code - order matters
document.addEventListener("DOMContentLoaded", function() {
    createBoard();
    setInitialPositions();
    setSafePositions(); // Set safe positions after initial positions
    addStartarrows(); // Add start arrows to the board
    calculateStartingPathPositions();
    playerTurn();
});
