function nextMove() {

    if (currentMove < moves.length) {

        let move = moves[currentMove];

        game.move({
            from: move.slice(0, 2),
            to: move.slice(2, 4),
            promotion: 'q'
        });

        currentMove++;

        renderMoveTable();

        updateBoard();
    }
}

function previousMove() {

    if (currentMove > 0) {

        game.undo();

        currentMove--;

        renderMoveTable();

        updateBoard();
    }
}

function togglePlay() {

    if (currentMove >= moves.length) {

        game.reset();

        currentMove = 0;

        renderMoveTable();

        updateBoard();
    }

    if (autoplay === null) {

        autoplay = setInterval(function () {

            if (currentMove < moves.length) {

                nextMove();

            } else {

                clearInterval(autoplay);

                autoplay = null;
            }

        }, 1000);

    } else {

        clearInterval(autoplay);

        autoplay = null;
    }
}

document.getElementById("play-btn").onclick = togglePlay;
document.getElementById("next-btn").onclick = nextMove;
document.getElementById("back-btn").onclick = previousMove;

document.addEventListener("keydown", function(event) {

    if (document.activeElement.tagName.toLowerCase() === "textarea") return;

    if (event.code === "ArrowRight") {

        event.preventDefault();

        nextMove();

    } else if (event.code === "ArrowLeft") {

        event.preventDefault();

        previousMove();

    } else if (event.code === "Space") {

        event.preventDefault();

        togglePlay();
    }
});