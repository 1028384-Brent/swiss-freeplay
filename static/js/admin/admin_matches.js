document.addEventListener('DOMContentLoaded', function() {
    fetchMatches();
});

function fetchMatches() {
    fetch('/api/matches')
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            const tableBody = document.querySelector('#matches tbody');
            tableBody.innerHTML = ''; // Clear existing content

            if (data.status === 'success' && data.matches.length > 0) {
                const busyCourts = data.matches
                    .filter(m => m.court != null)
                    .map(m => m.court);

                data.matches.forEach(match => {
                    const tr = document.createElement('tr');

                    let buttonsHtml = '';

                    if (!match.court) {
                        data.courts.forEach(court => {
                            const isBusy = busyCourts.includes(court.id);

                            if (!isBusy) {
                                buttonsHtml += `
                                <button class="btn-assign" onclick="assignCourt(${match.game_id}, ${court.id})">
                                    ${court.number}
                                </button>`;
                            }
                        });
                    } else {
                        buttonsHtml = `<span>Toegewezen aan Baan ${match.court}</span>`;
                    }

                    tr.innerHTML = `
                          <td>Player ${match.t1_p1} & Player ${match.t1_p2}</td>
                          <td>Player ${match.t2_p1} & Player ${match.t2_p2}</td>
                          <td>${getStatusLabel(match.status)}</td>
                          <td>${buttonsHtml}</td
                    `;
                    tableBody.appendChild(tr);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="4">No matches found.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });
}

function getStatusLabel(statusCode) {
    const statuses = {
        1: 'Completed',
        2: 'Scheduled',
        3: 'In Progress'
    };
    return statuses[statusCode] || 'Unknown';
}

function assignCourt(gameId, courtId) {
    fetch('/admin/api/assign_court', {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({ game_id: gameId, court_id: courtId})
    })
    .then(response => response.json())
    .then(result => {
        if (result.status === 'success') {
            alert('Baan toegewezen!');
            fetchMatches();
        } else {
            alert('Fout: ' + result.message);
        }
    });
}