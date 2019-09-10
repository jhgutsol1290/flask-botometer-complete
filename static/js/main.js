let countBot = 0
let countReal = 0
let notAccount = 0
let status = document.getElementsByClassName('status')
let arrayStatus = Array.from(status)
let newArrayStatus = arrayStatus.map(el=>el.textContent)
let botsDOM = document.getElementById('bots-count')
let realDOM = document.getElementById('real-count')
let totalDOM = document.getElementById('total-count')


newArrayStatus.map(el=>{
    if(el === 'Bot'){
        countBot += 1
    }else if(el === 'Real Account'){
        countReal += 1
    }else{
        notAccount += 1
    }
})


console.log('Bots: ', countBot)
console.log('Real: ', countReal)
console.log('Not Account', notAccount)

let array = [countBot, countReal]

botsDOM.textContent = countBot
realDOM.textContent = countReal
totalDOM.textContent = countBot + countReal


var config = {
    type: 'pie',
    data: {
        datasets: [{
            data: array,
            backgroundColor: [
                '#ff8080',
                '#c6f1d6',
            ],
            label: 'Dataset 1'
        }],
        labels: [
            'Bots',
            'Cuentas Reales',  
        ]
    },
    options: {
        responsive: true
    }
};

window.onload = function() {
    var ctx = document.getElementById('canvas').getContext('2d');
    window.myPie = new Chart(ctx, config);
};