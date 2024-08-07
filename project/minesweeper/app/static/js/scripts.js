document.addEventListener("DOMContentLoaded", function() {
    const grid = document.getElementById("minesweeper-grid");

    // Event listener for cell clicks
    grid.addEventListener("click", function(event) {
        if (event.target && event.target.nodeName === "TD") {
            const cell = event.target;
            const row = cell.parentNode.rowIndex;
            const col = cell.cellIndex;

            revealCell(row, col);
        }
    });

    // Event listener for right-click (context menu) to flag a cell
    grid.addEventListener("contextmenu", function(event) {
        event.preventDefault();
        if (event.target && event.target.nodeName === "TD") {
            const cell = event.target;
            const row = cell.parentNode.rowIndex;
            const col = cell.cellIndex;

            flagCell(row, col);
        }
    });

    // Function to reveal a cell
    function revealCell(row, col) {
        fetch(`/reveal/${row}/${col}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            updateGrid(data.grid);
            if (data.game_over) {
                alert("Game Over! You hit a mine.");
                // Optionally, you can reset the game or offer a restart option here
            }
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to flag a cell
    function flagCell(row, col) {
        fetch(`/flag/${row}/${col}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            updateGrid(data.grid);
        })
        .catch(error => console.error('Error:', error));
    }

    // Function to update the grid based on the game state
    function updateGrid(gridData) {
        for (let row = 0; row < gridData.length; row++) {
            for (let col = 0; col < gridData[row].length; col++) {
                const cell = grid.rows[row].cells[col];
                const cellData = gridData[row][col];

                if (cellData.revealed) {
                    cell.classList.add("revealed");
                    if (cellData.mine) {
                        cell.classList.add("mine");
                        cell.textContent = "💣";
                    } else if (cellData.number > 0) {
                        cell.textContent = cellData.number;
                    }
                } else if (cellData.flagged) {
                    cell.classList.add("flagged");
                    cell.textContent = "🚩";
                } else {
                    cell.classList.remove("revealed", "mine", "flagged");
                    cell.textContent = "";
                }
            }
        }
    }
});
