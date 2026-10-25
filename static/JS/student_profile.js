// page loads first
document.addEventListener('DOMContentLoaded',function () {

    //fetch data from the flask API
    fetch(`/student/api/profile_subjects/${studentId}`)
        .then(response => response.json())
        .then(data => {
            const student_subjects = document.getElementById('student_subjects');

            student_subjects.innerText = data.subject_name.join(", ")
        })

    fetch(`/student/api/myteachers/${studentId}`)
        .then(response => response.json())
        .then(data => {
            const student_myteachers = document.getElementById('student_myteachers');

            student_myteachers.innerText = data.teacher_name.join(", ")
        })

    fetch(`/student/api/name/${studentId}`)
        .then(response => response.json())
        .then(data => {
            const student_name = document.getElementById('student_name');
            const student_email_name = document.getElementById('student_email_name');
            const student_title_name = document.getElementById('student_title_name')

            student_name.innerText = data.student_name
            student_email_name.innerText = data.student_name
            student_title_name.innerText = data.student_name
        })

    //fetch data from the flask API
    fetch(`/student/api/profile_grades/${studentId}`)
        .then(response => response.json())
        .then(data => {
            const biology_grade = document.getElementById('biology_grade');
            const physics_grade = document.getElementById('physics_grade');
            const science_grade = document.getElementById('science_grade');
            const math_grade = document.getElementById('math_grade');
            const warning = document.getElementById('low_grade');
            const average = document.getElementById('average_grade');
            const motivation = document.getElementById('motivation');


            biology_grade.innerText = (data.student_biology[2] * 10).toFixed(1);
            physics_grade.innerText = (data.student_physics[2] * 10).toFixed(1);
            science_grade.innerText = (data.student_science[2] * 10).toFixed(1);
            math_grade.innerText = (data.student_math[2] * 10).toFixed(1);


            const grades = {
                Biologie: data.student_biology[2],
                Natuurkunde: data.student_physics[2],
                Scheikunde: data.student_science[2],
                Wiskunde: data.student_math[2]
            };

            const average_grade = Object.values(grades).reduce((a, b) => a + b) / 4;
            const average_grade_formatted = (average_grade * 10).toFixed(1)

            if (average_grade < 0.55)
            {
                motivation.innerText = "⚠ Je kunt nog een inhaalslag  maken!"
                motivation.style.color = "red"
                motivation.style.fontWeight = "bold"
                average.innerText = `Je gemiddelde cijfer van al jouw vakken is ${average_grade_formatted} / 10`
                average.style.fontStyle = "italic"
            }
            else
            {
                motivation.innerText = "✔ Lekker bezig, je resultaat is op niveau!"
                motivation.style.color = "green"
                motivation.style.fontWeight = "bold"
                average.innerText = `Je gemiddelde cijfer van al jouw vakken is ${average_grade_formatted} / 10`
                average.style.fontStyle = "italic"
            }

            let weakGrades = [];

            for (const subject in grades) {
                if (grades[subject] < 0.55) {
                    weakGrades.push(`${subject}: ${(grades[subject] * 10).toFixed(1)}`);
                }
            }

            if (weakGrades.length > 0)
            {
                warning.innerText = weakGrades.join("<br>");
                warning.style.color = "Brown" //"coral"
                warning.style.fontWeight = "bold"
            }
    })
})
