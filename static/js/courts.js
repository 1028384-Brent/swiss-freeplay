document.addEventListener('DOMContentLoaded', () => {
    updateCourtTable();

    setInterval(updateCourtTable, 30000);
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

            if (assignedMatch) {
                cellTeam1.textContent = `${assignedMatch.t1_p1} & ${assignedMatch.t1_p2}`;
                cellTeam2.textContent = `${assignedMatch.t2_p1} & ${assignedMatch.t2_p2}`;

                row.style.backgroundColor = "#e6ffe6";
            } else{
                cellTeam1.textContent = "_";
                cellTeam2.textContent = "_";
                row.style.backgroundColor = "_";
            }
        });
    } catch (error) {
        console.error("Error fetching court data:", error);
    }
}