document.addEventListener('DOMContentLoaded', function() {
    fetchMatches();
    setInterval(fetchMatches, 10000);

});

function fetchMatches() {
    fetch('/api/matches')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const tableBody = document.querySelector('#matches tbody');
            tableBody.innerHTML = ''; // Clear existing content

            if (data.status === 'success' && data.matches.length > 0) {
                data.matches.forEach(match => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                          <td>Player ${match.t1_p1} & Player ${match.t1_p2}</td>
                          <td>Player ${match.t2_p1} & Player ${match.t2_p2}</td>
                          <td>${getStatusLabel(match.status)}</td>
                    `;
                    tableBody.appendChild(tr);
                });
            } else {
                tableBody.innerHTML = '<tr><td colspan="3">No matches found.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching matches:', error);
        });
}

function getStatusLabel(statusCode) {
    // Mapping the integer status from your database to readable text
    const statuses = {
        1: 'In progress',
        2: 'Scheduled', // Based on your INSERT statement using status 2
        3: 'Completed'
    };
    return statuses[statusCode] || 'Unknown';
}