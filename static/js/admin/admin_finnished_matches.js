document.addEventListener('DOMContentLoaded', function() {
    fetchFinishedMatches();
    // Refresh every 30 seconds since finished matches change less frequently
    setInterval(fetchFinishedMatches, 30000);
});

function fetchFinishedMatches() {
    fetch('/admin/api/finished_matches')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#matches tbody');
            if (!tableBody) return;

            tableBody.innerHTML = '';

            if (data.status === 'success' && Array.isArray(data.matches)) {
                const finishedMatches = data.matches.filter(match => match.status == 3);

                finishedMatches.forEach(match => {
                    const tr = document.createElement('tr');

                    // Prepare labels for the prompt
                    const team1 = `${match.t1_p1 || 'P1'} & ${match.t1_p2 || 'P2'}`;
                    const team2 = `${match.t2_p1 || 'P3'} & ${match.t2_p2 || 'P4'}`;

                    tr.innerHTML = `
                        <td>${team1}</td>
                        <td>${team2}</td>
                        <td><span class="status-badge">Finished</span></td>
                        <td>
                            <button class="btn-score" onclick="toggleScore(${match.id})">View Score</button>
                            <div id="score-${match.id}" style="display:none;">
                                <strong>${match.score_team_1} - ${match.score_team_2}</strong>
                            </div>
                        </td>
                        <td>
                            <button class="btn-edit" onclick="enterScore(${match.id}, '${team1}', '${team2}')">
                                Edit Score
                            </button>
                        </td>
                    `;
                    tableBody.appendChild(tr);
                });
            }
        });
}

/**
 * Sends score data to the Flask @app.route('/api/score')
 */
async function enterScore(gameId, team1Name, team2Name) {
    const s1 = prompt(`Score voor ${team1Name}:`);
    const s2 = prompt(`Score voor ${team2Name}:`);

    // Validation
    if (s1 === null || s2 === null) return;
    const score1 = parseInt(s1);
    const score2 = parseInt(s2);

    if (isNaN(score1) || isNaN(score2)) {
        alert("Voer a.u.b. geldige getallen in.");
        return;
    }

    try {
        const response = await fetch('/api/score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                game_id: gameId,    // Matches 'game_id' in Flask
                score_t1: score1,   // Matches 'score_t1' in Flask
                score_t2: score2    // Matches 'score_t2' in Flask
            })
        });

        const result = await response.json();
        if (result.status === 'success') {
            alert("Score succesvol bijgewerkt!");
            fetchFinishedMatches(); // Refresh the table
        } else {
            alert("Fout: " + result.message);
        }
    } catch (error) {
        console.error("Fetch error:", error);
    }
}

// Make sure it's accessible globally
window.enterScore = enterScore;
window.toggleScore = function(id) {
    const el = document.getElementById(`score-${id}`);
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
};