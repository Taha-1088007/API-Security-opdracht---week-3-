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

            let on_level = 0;

            for (const subject in grades)
            {
                const grade = grades[subject];

                if (grade >= 0.55) on_level++
            }

            const on_level_HTML = document.getElementById('on-level');
            on_level_HTML.innerText = on_level + " van 4"
    })
})
