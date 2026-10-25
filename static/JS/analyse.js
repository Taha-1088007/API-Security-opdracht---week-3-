console.log("JS loaded");

const TAXONOMY_COLORS = {
  "Onthouden":  { bg: "rgba(54, 162, 235, 0.7)",  border: "rgb(54, 162, 235)" },
  "Begrijpen":  { bg: "rgba(75, 192, 192, 0.7)",   border: "rgb(75, 192, 192)" },
  "Toepassen":  { bg: "rgba(255, 205, 86, 0.7)",   border: "rgb(255, 205, 86)" },
  "Analyseren": { bg: "rgba(255, 99, 132, 0.7)",   border: "rgb(255, 99, 132)" },
  "Evalueren":  { bg: "rgba(153, 102, 255, 0.7)",  border: "rgb(153, 102, 255)" },
  "Creëren":    { bg: "rgba(255, 159, 64, 0.7)",   border: "rgb(255, 159, 64)" },
};

window.onload = async function () {
  const res = await fetch(`/teacher/api/analyse/${teacherId}`);
  const raw = await res.json();

  // Collect unique students and taxonomy levels
  const studentMap = {};
  const taxonomySet = new Set();

  raw.forEach(({ student_name, taxonomy_level, student_score }) => {
    if (!studentMap[student_name]) studentMap[student_name] = {};
    studentMap[student_name][taxonomy_level] = student_score;
    taxonomySet.add(taxonomy_level);
  });

  const students = Object.keys(studentMap);
  const taxonomies = [...taxonomySet];

  // One dataset per taxonomy level
  const datasets = taxonomies.map(tax => ({
    label: tax,
    data: students.map(s => +((studentMap[s][tax] ?? 0) * 10).toFixed(1)),
    backgroundColor: (TAXONOMY_COLORS[tax] || { bg: "rgba(200,200,200,0.7)" }).bg,
    borderColor:     (TAXONOMY_COLORS[tax] || { border: "rgb(200,200,200)" }).border,
    borderWidth: 1,
  }));

  new Chart(document.getElementById("myChart"), {
    type: "bar",
    data: { labels: students, datasets },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Scores per leerling per taxonomieniveau" },
      },
      scales: {
        y: { beginAtZero: true, max: 10, title: { display: true, text: "Score" } },
        x: { beginAtZero: true, max: 10, title: { display: true, text: "Leerling" } },
      },
    },
  });

  //function get_lowest_taxonomy() {
      let count_analyseren = 0;
      let count_begrijpen = 0;
      let count_onthouden = 0;
      let count_toepassen = 0;

      fetch(`/teacher/api/analyse/${teacherId}`)
          .then(response => response.json())
          .then(data => {


              for (let i = 0; i < data.length; i++) {

                  const student_score = data[i].student_score
                  const taxonomy_level = data[i].taxonomy_level

                  //check the taxonomy levels below 5.5 zijn &
                  // (later) choose from the two that appear the most the keywords/subjects that need to be taught more in class
                  if (student_score < 0.55 && taxonomy_level == "Analyseren") count_analyseren++;

                  if (student_score < 0.55 && taxonomy_level == "Begrijpen") count_begrijpen++;

                  if (student_score < 0.55 && taxonomy_level == "Onthouden") count_onthouden++;

                  if (student_score < 0.55 && taxonomy_level == "Toepassen") count_toepassen++;
              }

              console.log(count_analyseren, count_begrijpen, count_onthouden, count_toepassen);

              var insufficient_taxonomy = [count_analyseren, count_begrijpen, count_onthouden, count_toepassen];
              var taxonomy_levels = ["Analyseren", "Begrijpen", "Onthouden", "Toepassen"];

              var lowest_taxonomy = Math.max.apply(null, insufficient_taxonomy); // get the max of the array
              var store_lowest_taxonomy = insufficient_taxonomy.indexOf(lowest_taxonomy);

              insufficient_taxonomy.splice(insufficient_taxonomy.indexOf(lowest_taxonomy), 1); // remove max from the array

              var second_lowest_taxonomy = Math.max.apply(null, insufficient_taxonomy); // get the 2nd max
              var store_second_lowest_taxonomy = insufficient_taxonomy.indexOf(second_lowest_taxonomy);


              //get names
              lowest_taxonomy_name = taxonomy_levels[store_lowest_taxonomy];
              second_lowest_taxonomy_name = taxonomy_levels[store_second_lowest_taxonomy];


              const lowest_taxonomy_html = document.getElementById('lowest_taxonomy');
              const second_lowest_taxonomy_html = document.getElementById('second_lowest_taxonomy');
              const keywords_html_first = document.getElementById('keywords_first');
              //const keywords_html_second = document.getElementById('keywords_second');

              lowest_taxonomy_html.innerText = lowest_taxonomy_name;
              second_lowest_taxonomy_html.innerText = second_lowest_taxonomy_name;


              let keywords_first = ""
              let keywords_second = ""

              for (let i = 0; i < data.length; i++) {
                    if (lowest_taxonomy_name == data[i].taxonomy_level) {
                        keywords_first = JSON.parse(data[i].keywords).join(', ')
                        console.log(keywords_first)
                    }

                    else if (second_lowest_taxonomy_name == data[i].taxonomy_level) {
                        keywords_second = JSON.parse(data[i].keywords).join(', ')
                        //console.log(keywords_second)
                    }

                    else
                        console.log("failed")
                }

              keywords_html_first.innerText = keywords_first;
              //keywords_html_second.innerText = keywords_second;
          })
    //}
};
