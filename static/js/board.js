function onDrop(source, target) {

    let move = game.move({
        from: source,
        to: target,
        promotion: 'q'
    });

    if (move === null) {
        return 'snapback';
    }

    currentMove++;

    updateBoard();
}

function jumpToMove(targetMove) {

    game.reset();

    currentMove = 0;

    for (let i = 0; i < targetMove; i++) {

        let move = moves[i];

        game.move({
            from: move.slice(0, 2),
            to: move.slice(2, 4),
            promotion: 'q'
        });

        currentMove++;
    }

    updateBoard();
    renderMoveTable();
}

function updateBoard() {

    board.position(game.fen());

    updateEvalBar();

    renderMoveTable();

    let container = document.getElementById("engine-lines");

    container.innerHTML = "";

    let openingDiv = document.getElementById("opening-name");

    if (currentMove > 0) {

        let currentOpening = moveData[currentMove - 1].opening;

        if (currentOpening) {
            openingDiv.innerText = "Opening: " + currentOpening;
        } else {
            openingDiv.innerText = "Opening: Unknown";
        }

        let currentLines = allLines[currentMove - 1];

        currentLines.forEach(function(lineData) {

            container.innerHTML += `
                <div class="engine-line">

                    <span class="engine-eval">
                        ${lineData.eval > 0 ? "+" : ""}
                        ${lineData.eval/100}
                    </span>

                    <span class="engine-moves">
                        ${lineData.line}
                    </span>

                </div>
            `;
        });
    }
    else {
        openingDiv.innerText = "";
    }
}