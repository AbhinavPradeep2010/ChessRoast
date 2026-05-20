function renderMoveTable() {

    let table = document.getElementById("move-table");

    table.innerHTML = "";

    for (let i = 0; i < sanMoves.length; i += 2) {

        let row = document.createElement("div");

        row.className = "move-row";

        let moveNumber = Math.floor(i / 2) + 1;

        let whiteMove = sanMoves[i] || "";

        let blackMove = sanMoves[i + 1] || "";

        let whiteClassification = moveData[i]?.classification || "";

        let blackClassification = moveData[i + 1]?.classification || "";

        row.innerHTML = `
            <div class="move-cell move-number">
                ${moveNumber}
            </div>

            <div class="move-cell move-btn ${currentMove === i + 1 ? 'active-move' : ''}"
                id="${currentMove === i + 1 ? 'current-move' : ''}"
                onclick="jumpToMove(${i + 1})">
                ${whiteMove}
                <img
                    class="classification-icon"
                    src="/static/images/classifications/${whiteClassification}.png"
                >
            </div>

            <div class="move-cell move-btn ${currentMove === i + 2 ? 'active-move' : ''}"
                id="${currentMove === i + 2 ? 'current-move' : ''}"
                onclick="jumpToMove(${i + 2})">
                ${blackMove}
                <img
                    class="classification-icon"
                    src="/static/images/classifications/${blackClassification}.png"
                >
            </div>
        `;

        table.appendChild(row);
    }

    let currentMoveElement = document.getElementById("current-move");

    if (currentMoveElement) {

        currentMoveElement.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
}