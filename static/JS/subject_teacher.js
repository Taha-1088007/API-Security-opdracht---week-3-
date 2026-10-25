let myChartInstance= null;

window.onload = async function (){
    try{
        const response = await fetch(`/teacher/api/subject/${subjectId}`);
        const data = await response.json();

        if (!data || data.length ===0) return;

        // Prepare labels (student names) and data for the chart
        const labels = data.map(s => s.name);
        const knowledgeData = data.map (s => (parseFloat(s.kennen ||0).toFixed(1)));
        const skillsData = data.map (s => (parseFloat(s.kunnen ||0).toFixed(1)));

        // draw chart or refresh the chart
        const ctx = document.getElementById('classChart').getContext('2d');
        if (myChartInstance){
            myChartInstance.destroy();
        }
        myChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Kennen',
                        data: knowledgeData,
                        backgroundColor: 'rgba(14, 19, 71, 0.8)'
                    },
                    {
                        label: 'Kunnen',
                        data: skillsData,
                        backgroundColor: 'rgba(30, 78, 184, 0.6)'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {stacked: true},
                    y: {
                        stacked: true,
                        beginAtZero: true,
                        max: 10
                    }
                }
            }
        });

        // calculating class average
        const sum = data.reduce((acc, s) => {
            const kn = parseFloat(s.kennen) || 0;
            const ku = parseFloat(s.kunnen) || 0;
            return acc + (kn +ku);
        },0);

        // average score based on combined metrics of knowledge/skills
        const totalAvg = sum/data.length;
        const displayScore = totalAvg.toFixed(1);

        //UI elements for status feedback
        const statusBadge = document.getElementById('status-badge');
        const priorityText = document.getElementById('priority-text');
        const priorityTitle = document.getElementById('priority-title')

        // status update based on the class average
        if (totalAvg < 5.5) {
            statusBadge.className = 'status-score low';
            if(priorityTitle) priorityTitle.textContent ="Prioriteit Inhaalslag";
            if(priorityText) priorityText.innerHTML =
                "De klas scoort laag. Deze onderwerpen moeten <strong> opnieuw behandeld worden</strong>:";
        }else {
            statusBadge.className= 'status-score success';
            if(priorityTitle) priorityTitle.textContent ="Focus: Verdieping";
            if(priorityText) priorityText.textContent =
                "De klas presteert goed. Focus op verdieping van de volgende leerdoelen:"
        }
        if(statusBadge) statusBadge.textContent = `Klasgemiddelde: ${displayScore}`;

        // collect weak goals and keywords for students scoring below 5.5
        let allKeywords = [];
        let allGoals = [];
        data.forEach(s => {
            const studentAvg = (parseFloat(s.kennen || 0) + parseFloat(s.kunnen || 0));
            if(s.weak_goals && studentAvg <5.5) {
                allGoals.push(...s.weak_goals);

                // We remove all [, ], " and ' characters from the text
                const cleanString = s.keywords.replace(/[\[\]"']/g, '');
                // Then we split on the decimal point
                const split = cleanString.split(',').map(k => k.trim());
                allKeywords.push(...split)

            }
        });

        // Make unique and filter on empty values
        const uniqueKeywords = [...new Set(allKeywords.map(k=> k.trim ()))].filter(k=>k && k !=="");
        const uniqueGoals = [...new Set(allGoals.map(g=> g.trim ()))].filter(g=>g && g !=="");

        const learningGoalUl = document.getElementById('learning goal-list');
        if (learningGoalUl){
            learningGoalUl.innerHTML = uniqueGoals.map(g => `<li>${g}</li>`).join('');
        }

        // Divide between the two lists
        const half = Math.ceil(uniqueKeywords.length / 2);
        const knowledgeUl = document.getElementById('kennen-tags');
        const skillsUl = document.getElementById('kunnen-tags');
        if (knowledgeUl) {
            knowledgeUl.innerHTML = uniqueKeywords.slice(0, half)
                .map(k=> `<li>${k}</li>`).join('');
        }
        if (skillsUl){
             skillsUl.innerHTML = uniqueKeywords.slice(half).map(k=>`<li>${k}</li>`).join('');
        }

    } catch (error) {
    console.error("Fout:", error);
    }
};