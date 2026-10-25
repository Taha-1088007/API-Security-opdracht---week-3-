// page loads first
document.addEventListener('DOMContentLoaded',function () {

    //fetch data from the flask API
    fetch(`/student/api/profile_grades/${studentId}`)
        .then(response => response.json())
        .then(data => {

            console.log("JS Loaded")

            const grades = {
                Biologie: data.student_biology[2],
                Natuurkunde: data.student_physics[2],
                Scheikunde: data.student_science[2],
                Wiskunde: data.student_math[2]
            };

            for (const subject in grades)
            {
                const grade = grades[subject];

                let status = "";
                let statusClass = "";

                if (grade >= 0.45 && grade < 0.55){
                    status = "Blijf je best doen!"
                    statusClass = "status-risk"
                }
                else if (grade >= 0.55 && grade < 0.7){
                    status = "Lekker bezig!"
                    statusClass = "status-success"
                }
                else if (grade >= 0.7){
                    status = "Super goed bezig!"
                    statusClass = "status-perfect"
                }
                else if (grade < 0.45){
                    status = "Niet opgeven!"
                    statusClass = "status-help"
                }
                else{
                    status = "Nog geen resultaten.."
                    statusClass = "status-perfect"
                }
                console.log(subject, grade, status)

                const statusHTML = document.getElementById(`status-${subject}`);

                if (statusHTML){
                    statusHTML.innerText = status;
                    statusHTML.className = statusClass;
                }
            }
    })
})
