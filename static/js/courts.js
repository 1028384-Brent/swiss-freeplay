document.addEventListener('DOMContentLoaded', () => {
    updateCourtTable();

    setInterval(updateCourtTable, 10000);
});

async function updateCourtTable() {
    try{
        const response = await fetch('/api/matches');
        const data = await response.json();
        const tableBody = document.getElementById("court-table-body");

        tableBody.innerHTML = "";

        data.courts.forEach(court => {
            const row = tableBody.insertRow();
            const assignedMatch = data.matches.find(m => m.court === court.id);

            row.insertCell(0).textContent = court.number;
            row.insertCell(1).textContent = court.name;

            let cellTeam1 = row.insertCell(2);
            let cellTeam2 = row.insertCell(3);
            let cellAction = row.insertCell(4);

            if (assignedMatch) {
                const team1 = `${assignedMatch.t1_p1} & ${assignedMatch.t1_p2}`;
                const team2 = `${assignedMatch.t2_p1} & ${assignedMatch.t2_p2}`;

                cellTeam1.textContent = team1;
                cellTeam2.textContent = team2;
                row.style.backgroundColor = "#e6ffe6";

                const scoreBtn = document.createElement('button');
                scoreBtn.textContent = "Score invoeren";
                scoreBtn.className = "btn-score";
                scoreBtn.onclick = () => enterScore(assignedMatch.game_id, team1, team2);
                cellAction.appendChild(scoreBtn);
            } else{
                cellTeam1.textContent = "_";
                cellTeam2.textContent = "_";
                cellAction.textContent = "";
                row.style.backgroundColor = "";
            }
        });
    } catch (error) {
        console.error("Error fetching court data:", error);
    }
}

async function enterScore(gameId, team1Name, team2Name) {
    const s1 = prompt(`Score voor ${team1Name}:`);
    const s2 = prompt(`Score voor ${team2Name}:`);

    if (s1 === null || s2 === null) return;

    const score1 = parseInt(s1);
    const score2 = parseInt(s2);

    if (isNaN(score1) || isNaN(score2)){
        alert("Voer alsjeblieft geldige getallen in.");
        return;
    }

    if (score1 > 30 || score2 > 30) {
        alert("De maximale score is 30.");
        return;
    }

    if (score1 === 30 && score2 === 30) {
        alert("Beide teams kunnen niet 30 punten hebben. Er moet een winnaar zijn! ")
        return;
    }

    try{
        const response = await fetch('/api/score', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                game_id: gameId,
                score_t1: parseInt(s1),
                score_t2: parseInt(s2)
            })
        });

        const result = await response.json();
        if (result.status === 'success') {
            alert("Score verwerkt!");
            updateCourtTable(); // Ververs de tabel direct
        } else {
            alert("Fout bij opslaan: " + result.message);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}
