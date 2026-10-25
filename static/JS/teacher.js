// page loads first
document.addEventListener('DOMContentLoaded',function () {

    //fetch data from the flask API
    fetch('/teacher/api/class')
        .then(response => response.json())
        .then(data => {
            const tabelBody = document.getElementById('students-list');

            tabelBody.innerHTML = '';

            //loop through the list of students
            data.forEach(student => {

                let statusClass= '';
                let statusText ='';

                if (student.score >= 0.80) {
                statusClass = 'status-perfect';
                statusText = 'Uitblinkend';
                } else if (student.score >= 0.55) {
                    statusClass = 'status-success';
                    statusText = 'Op schema';
                } else {
                    statusClass = 'status-help';
                    statusText = 'Aandacht nodig';
                }

                const row =`
                <tr>
                    <td>${student.name}</td> 
                    <td><span class ="${statusClass}">${statusText}</span></td>
                    <td>
                        <a href="/teacher/class/details/${student.id}" class="action-btn">Details</a>
                    </td>
                </tr>`;

                //add row to the table body
                tabelBody.innerHTML +=row;
            })
        })
});