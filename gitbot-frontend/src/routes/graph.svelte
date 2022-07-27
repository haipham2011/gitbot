<script>
  import { onMount } from "svelte";
  import { Chart, registerables } from "chart.js";

  export let data;
  Chart.register(...registerables);
  let codeFreqCanvas;
  let commitActivityCanvas;

  onMount(() => {
    const ctxCodeFreq = codeFreqCanvas.getContext("2d");
    const ctxCommitActivity = commitActivityCanvas.getContext("2d");

    const { codeFrequency, commitActivity } = data;
    const codeFrequencyChart = new Chart(ctxCodeFreq, {
      type: "bar",
      data: {
        labels: ["Code addition", "Code deletion"],
        datasets: [
          {
            label: codeFrequency[0].name,
            data: [codeFrequency[0].addition, codeFrequency[0].deletion],
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
          {
            label: codeFrequency[1].name,
            data: [codeFrequency[1].addition, codeFrequency[1].deletion],
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
          {
            label: codeFrequency[2].name,
            data: [codeFrequency[2].addition, codeFrequency[2].deletion],
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            borderColor: "rgba(255, 206, 86, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: "Code change frequency",
          },
        },
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });

    const commitActivityChart = new Chart(ctxCommitActivity, {
      type: "line",
      data: {
        labels: commitActivity[0].activity.map((element) => element.week),
        datasets: [
          {
            label: commitActivity[0].name,
            data: commitActivity[0].activity.map((element) => element.total),
            lineTension: 0,
            fill: false,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
          },
          {
            label: commitActivity[1].name,
            data: commitActivity[1].activity.map((element) => element.total),
            lineTension: 0,
            fill: false,
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
          },
          {
            label: commitActivity[2].name,
            data: commitActivity[2].activity.map((element) => element.total),
            lineTension: 0,
            fill: false,
            backgroundColor: "rgba(255, 206, 86, 0.2)",
            borderColor: "rgba(255, 206, 86, 1)",
          },
        ],
      },
      options: {
        responsive: true,
        interaction: {
          mode: "index",
          intersect: false,
        },
        stacked: false,
        plugins: {
          title: {
            display: true,
            text: "Commit activity in weeks",
          },
        },
        scales: {
          y: {
            type: "linear",
            display: true,
            position: "left",
          },
          y1: {
            type: "linear",
            display: true,
            position: "right",

            // grid line settings
            grid: {
              drawOnChartArea: false, // only want the grid lines for one axis to show up
            },
          },
        },
      },
    });
  });
</script>

<canvas id="codeFrequencyChart" bind:this={codeFreqCanvas} />
<canvas id="commitActivityChart" bind:this={commitActivityCanvas} />

<style>
  canvas {
    width: 800px !important;
    height: 800px !important;
    margin-left: 20%;
  }
</style>
