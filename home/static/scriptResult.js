document.addEventListener('DOMContentLoaded', () => {
    const snpScore = parseInt(document.getElementById("snp_score").innerHTML);
    const msciScore = document.getElementById("msci_score");
    const stockChange = document.getElementById("stockChange");

    // MSCI chart update
    switch (msciScore.innerHTML) {
        case "CCC":
            document.getElementById("th-1").style.backgroundColor = "red";
            break;
        case "B":
            document.getElementById("th-2").style.backgroundColor = "orangered";
            break;
        case "BB":
            document.getElementById("th-3").style.backgroundColor = "darksalmon";
            break;
        case "BBB":
            document.getElementById("th-4").style.backgroundColor = "goldenrod";
            break;
        case "A":
            document.getElementById("th-5").style.backgroundColor = "gold";
            break;
        case "AA":
            document.getElementById("th-6").style.backgroundColor = "lightgreen";
            break;
        case "AAA":
            document.getElementById("th-7").style.backgroundColor = "forestgreen";
            break;
        default:
            msciScore.innerHTML = "N/A";
    }

    // SnP chart update
    if (snpScore >= 0 && snpScore <= 100) {
        document.querySelector(".gauge_fill").style.transform = `rotate(${snpScore/200}turn)`;
        if (snpScore < 25) {
            document.querySelector(".gauge_fill").style.background = "red";
        } else if (snpScore >= 25 && snpScore < 50) {
            document.querySelector(".gauge_fill").style.background = "gold";
        } else if (snpScore >= 50 && snpScore < 75) {
            document.querySelector(".gauge_fill").style.background = "lightgreen";
        } else if (snpScore >= 75) {
            document.querySelector(".gauge_fill").style.background = "forestgreen";
        }
    } else if (isNaN(snpScore)) {
        document.getElementById("snp_score").innerHTML = "N/A";
        document.querySelector(".gauge_fill").style.transform = 'rotate(0turn)';
    }

    // Stock price change
    if (stockChange.innerHTML < 0) {
        stockChange.style.color = "red";
        document.getElementById("priceChangeArrowUp").className = "d-none";
        document.getElementById("priceChangeArrowDown").className = "d-inline";
    } else if (stockChange.innerHTML >= 0) {
        stockChange.style.color = "green";
        document.getElementById("priceChangeArrowUp").className = "d-inline";
        document.getElementById("priceChangeArrowDown").className = "d-none";
    }

    // Chart
    let id = JSON.parse(document.getElementById("stockId").textContent);
    fetch(`chartdata/${id}`)
    .then(response => response.json())
    .then(result => {
        let labels = []
        let companyScores = []
        let industryScores = []

        const data = result['data']

        for(var key in data) {
            var value = data[key];

            labels.push(key);
            companyScores.push(value[0]);
            industryScores.push(value[1]);
        }

        const ctx = document.querySelector("#myChart").getContext("2d");
        new Chart(ctx, {
            type: 'bar',
            data: {
            labels: labels,
            datasets: [{
                type: 'bar',
                label: 'Company',
                data: companyScores,
                borderColor: 'rgb(127, 255, 212)',
                backgroundColor: 'rgb(127, 255, 212)',
                order: 2
            }, {
                type: 'line',
                label: 'Industry',
                data: industryScores,
                fill: false,
                borderColor: 'rgb(54, 162, 235)',
                order: 1
            }]
            },
            options: {
            scales: {
                y: {
                beginAtZero: true
                }
            }
            }
        });
    })
});

