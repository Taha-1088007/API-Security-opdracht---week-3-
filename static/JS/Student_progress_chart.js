console.log("JS loaded");

const SUBJECTS = [
  { id: 12, label: "Biologie",    canvasId: "chartBiology" },
  { id: 21, label: "Natuurkunde", canvasId: "chartPhysics" },
  { id: 22, label: "Scheikunde",  canvasId: "chartChem"    },
  { id: 31, label: "Wiskunde",    canvasId: "chartMath"    },
];

const SUBJECT_COLORS = {
  12: { bg: "rgba(54, 162, 235, 0.2)",  border: "rgb(54, 162, 235)"  },  // Biologie
  21: { bg: "rgba(255, 99, 132, 0.2)",  border: "rgb(255, 99, 132)"  },  // Natuurkunde
  22: { bg: "rgba(75, 192, 192, 0.2)",  border: "rgb(75, 192, 192)"  },  // Scheikunde
  31: { bg: "rgba(255, 205, 86, 0.2)",  border: "rgb(255, 205, 86)"  },  // Wiskunde
};


async function loadChart(subject) {
  const res = await fetch(`/student/api/student_progress_chart/${studentId}/${subject.id}`);
  const raw = await res.json();

  if (!raw.length) return; // no data for this subject, skip

  const labels = raw.map(d => d.snapshot_date);
  const scores = raw.map(d => ((d.student_score ?? 0) * 10).toFixed(1));
  const color = SUBJECT_COLORS[subject.id];

    new Chart(document.getElementById(subject.canvasId), {
    type: "line",                                          // ✅ line chart over time
    data: {
      labels,
      datasets: [{
        label: subject.label,
        data: scores,
        backgroundColor: color.bg,
        borderColor: color.border,
        borderWidth: 2,
        tension: 0.3,
        fill: true,
        pointRadius: 4,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: `Voortgang — ${subject.label}` },
        tooltip: {
          callbacks: {
            afterLabel: (ctx) => {
                  const kw = raw[ctx.dataIndex]?.keywords;
                  const goals = entry?.learning_goals ?? "-"
                  return [
                      `Kennen: ${(entry?.kennen *10).toFixed(1)}`,
                      `Kunnen: ${(entry?.kunnen *10).toFixed(1)}`,
                      `Leerdoelen: ${goals}`
                  ]
            }
          }
        }
      },
      scales: {
        y: { beginAtZero: true, max: 10, title: { display: true, text: "Score (0-10)" } },
        x: { title: { display: true, text: "Datum" } },
      },
    },
  });

  return raw;
}

window.onload = async function () {
  // load all 4 charts in parallel
  const results = await Promise.all(SUBJECTS.map(loadChart));

  // sidebar: use all data combined to find the 2 lowest taxonomy levels
  const allData = results.flat().filter(Boolean);
  const levelMap = {};
  allData.forEach(d => {
    if (!levelMap[d.taxonomy_level]) levelMap[d.taxonomy_level] = [];
    levelMap[d.taxonomy_level].push(d.student_score ?? 0);
  });

  const averaged = Object.entries(levelMap).map(([level, scores]) => ({
    taxonomy_level: level,
    student_score: scores.reduce((a, b) => a + b, 0) / scores.length,
    keywords: allData.find(d => d.taxonomy_level === level)?.keywords ?? "-",
  }));

  const sorted = averaged.sort((a, b) => a.student_score - b.student_score);

  document.getElementById("lowest_taxonomy").innerText = sorted[0]?.taxonomy_level ?? "-";
  document.getElementById("second_lowest_taxonomy").innerText = sorted[1]?.taxonomy_level ?? "-";
  document.getElementById("keywords_first").innerText = sorted[0]?.keywords ?? "-";
};