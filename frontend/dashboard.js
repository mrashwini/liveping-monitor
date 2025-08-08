const apiURL = "http://localhost:8000/logs";

async function fetchLogs() {
  try {
    const res = await fetch(apiURL);
    const data = await res.json();
    updateCharts(data);
    updateDowntimeList(data);
  } catch (error) {
    console.error("Error fetching logs:", error);
  }
}

let statusChart, responseChart;

function updateCharts(logs) {
  const timestamps = logs.map(log => new Date(log.timestamp).toLocaleTimeString());
  const statuses = logs.map(log => log.status === "UP" ? 1 : 0);
  const responseTimes = logs.map(log => log.response_time);

  if (!statusChart) {
    const ctx1 = document.getElementById("statusChart").getContext("2d");
    statusChart = new Chart(ctx1, {
      type: "line",
      data: {
        labels: timestamps,
        datasets: [{
          label: "Status (1=Up, 0=Down)",
          data: statuses,
        }]
      }
    });
  } else {
    statusChart.data.labels = timestamps;
    statusChart.data.datasets[0].data = statuses;
    statusChart.update();
  }

  if (!responseChart) {
    const ctx2 = document.getElementById("responseChart").getContext("2d");
    responseChart = new Chart(ctx2, {
      type: "line",
      data: {
        labels: timestamps,
        datasets: [{
          label: "Response Time (ms)",
          data: responseTimes,
        }]
      }
    });
  } else {
    responseChart.data.labels = timestamps;
    responseChart.data.datasets[0].data = responseTimes;
    responseChart.update();
  }
}

function updateDowntimeList(logs) {
  const list = document.getElementById("downtimeList");
  list.innerHTML = "";
  logs.filter(log => log.status !== "UP").forEach(log => {
    const li = document.createElement("li");
    li.textContent = `${log.timestamp} - ${log.url} - ${log.status}`;
    list.appendChild(li);
  });
}

fetchLogs();
setInterval(fetchLogs, 15000);
