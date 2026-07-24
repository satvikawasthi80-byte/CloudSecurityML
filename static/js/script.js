document.addEventListener("DOMContentLoaded", function () {

    // Pie Chart
    const chartCanvas = document.getElementById("pieChart");

    if (chartCanvas) {

        new Chart(chartCanvas, {

            type: "pie",

            data: {

                labels: [
                    "Normal Logs",
                    "Anomaly Logs"
                ],

                datasets: [{

                    data: [
                        normal,
                        anomaly
                    ],

                    backgroundColor: [
                        "#00ff95",
                        "#ff4d4d"
                    ],

                    borderColor: "#0d1117",

                    borderWidth: 2

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        labels: {

                            color: "white",

                            font: {
                                size: 16
                            }

                        }

                    }

                }

            }

        });

    }

    // Search Table
    const searchBox = document.getElementById("searchInput");

    if (searchBox) {

        searchBox.addEventListener("keyup", function () {

            let value = this.value.toLowerCase();

            let rows = document.querySelectorAll("table tbody tr");

            rows.forEach(function (row) {

                let text = row.innerText.toLowerCase();

                row.style.display =
                    text.includes(value)
                        ? ""
                        : "none";

            });

        });

    }

});