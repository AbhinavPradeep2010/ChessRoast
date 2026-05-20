function updateEvalBar() {

    let evalScore = 0;

    if (currentMove > 0) {
        evalScore = evals[currentMove - 1];
    }

    let whiteText = document.getElementById("eval-white-text");

    let blackText = document.getElementById("eval-black-text");

    whiteText.innerText = "";
    blackText.innerText = "";

    if (typeof evalScore === "string" && evalScore.includes("M")) {

        if (evalScore.startsWith("-")) {

            document.getElementById("eval-white").style.height = "0%";

            blackText.innerText = evalScore;

        } else {

            document.getElementById("eval-white").style.height = "100%";

            whiteText.innerText = "+" + evalScore;
        }

        return;
    }

    evalScore = Math.max(-1000, Math.min(1000, evalScore));

    let percentage = ((evalScore + 1000) / 2000) * 100;

    document.getElementById("eval-white").style.height =
        percentage + "%";

    let displayEval = (evalScore / 100).toFixed(1);

    if (evalScore >= 0) {

        whiteText.innerText = "+" + displayEval;

    } else {

        blackText.innerText = displayEval;
    }
}