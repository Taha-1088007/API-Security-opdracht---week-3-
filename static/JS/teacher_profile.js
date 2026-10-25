// page loads first
document.addEventListener('DOMContentLoaded',function () {

    //fetch data from the flask API
    fetch('/teacher/api/mystudents')
        .then(response => response.json())
        .then(data => {
            const paragraph = document.getElementById('my_students');

            let names = "";

            data.forEach(student => { names += student.name + ", "});
            paragraph.innerText = names.slice(0, -2);
        })

    //fetch data from the flask API
    fetch(`/teacher/api/profile_details/${teacherId}`)
        .then(response => response.json())
        .then(data => {
            const teacher_name = document.getElementById('teacher_name');

            const teacher_email_name = document.getElementById('teacher_email_name');

            const teacher_subject = document.getElementById('subject_name');

            const teacher_title_name = document.getElementById('teacher_title_name');


            teacher_name.innerText = data.teacher_name
            teacher_email_name.innerText = data.teacher_name
            teacher_subject.innerText = data.subject_name
            teacher_title_name.innerText = data.teacher_name
        })
})
