from bottle import route, run, request, response
import json
import time
import game
import config
from controllers.distance_sensor import SensorController
from controllers.arrow_keys import ArrowKeyController
import pygame as pg
from notifications import send_sms

@route('/')
def home():
    return '''<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Touchless Pong</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, sans-serif;
            background: #111;
            color: #fff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            width: 90%;
            max-width: 400px;
            text-align: center;
        }
        h1 { font-size: 2rem; margin-bottom: 0.5rem; }
        .subtitle { color: #888; margin-bottom: 2rem; }

        .screen { display: none; }
        .screen.active { display: block; }

        label { display: block; text-align: left; margin-bottom: 0.25rem; color: #aaa; font-size: 0.85rem; }
        select, input {
            width: 100%;
            padding: 12px;
            margin-bottom: 1rem;
            border-radius: 8px;
            border: 1px solid #333;
            background: #222;
            color: #fff;
            font-size: 1rem;
        }
        button {
            width: 100%;
            padding: 14px;
            border-radius: 8px;
            border: none;
            background: #4CAF50;
            color: #fff;
            font-size: 1.1rem;
            cursor: pointer;
            margin-top: 0.5rem;
        }
        button:hover { background: #45a049; }

        .spinner {
            width: 40px; height: 40px;
            border: 4px solid #333;
            border-top: 4px solid #4CAF50;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 2rem auto;
        }
        @keyframes spin { to { transform: rotate(360deg); } }

        .stat-box {
            background: #222;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 0.75rem;
        }
        .stat-value { font-size: 1.5rem; font-weight: bold; }
        .stat-label { color: #888; font-size: 0.85rem; }
        .win { color: #4CAF50; }
        .lose { color: #e74c3c; }
    </style>
</head>
<body>
<div class="container">

    <!-- SETUP SCREEN -->
    <div id="setup" class="screen active">
        <h1>Touchless Pong</h1>
        <p class="subtitle">Configure and start your game</p>

        <label>Controller</label>
        <select id="controller">
            <option value="sensor">Distance sensor</option>
            <option value="keyboard">Arrow keys</option>
        </select>

        <label>Phone number (optional)</label>
        <input type="tel" id="phone" placeholder="+1234567890">

        <label>Email (optional)</label>
        <input type="email" id="email" placeholder="you@example.com">

        <button onclick="startGame()">Start Game</button>
    </div>

    <!-- IN PROGRESS SCREEN -->
    <div id="playing" class="screen">
        <h1>Game in progress</h1>
        <p class="subtitle">Look at the Pi's screen!</p>
        <div class="spinner"></div>
    </div>

    <!-- RESULTS SCREEN -->
    <div id="results" class="screen">
        <h1 id="result-title"></h1>
        <div id="stats-container"></div>
        <button onclick="showSetup()">Play Again</button>
        <button onclick="quitGame()" style="background: #e74c3c; margin-top: 0.5rem;">Quit</button>
    </div>

</div>
<script>
function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

function showSetup() { showScreen('setup'); }

function startGame() {
    showScreen('playing');

    const data = {
        controller: document.getElementById('controller').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value
    };

    fetch('/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(r => r.json())
    .then(stats => {
        document.getElementById('result-title').textContent =
            stats.winner === 'player' ? 'You won!' : 'You lost';
        document.getElementById('result-title').className =
            stats.winner === 'player' ? 'win' : 'lose';

        const mins = Math.floor(stats.duration_seconds / 60);
        const secs = stats.duration_seconds % 60;

        document.getElementById('stats-container').innerHTML =
            '<div class="stat-box"><div class="stat-value">' +
                stats.player_score + ' - ' + stats.opponent_score +
            '</div><div class="stat-label">Final score</div></div>' +
            '<div class="stat-box"><div class="stat-value">' +
                mins + 'm ' + secs + 's' +
            '</div><div class="stat-label">Duration</div></div>';

        showScreen('results');
    })
    .catch(err => {
        alert('Game error: ' + err);
        showSetup();
    });
}

function quitGame() {
    fetch('/quit', { method: 'POST' })
    document.body.innerHTML = '<div style="display:flex; justify-content:center;align-items:center;height:100vh;color:#888;">Server stopped. You can close this tab.</div>';
}
</script>
</body>
</html>'''


@route('/start', method='POST')
def start_game():
    data = request.json

    if data['controller'] == 'sensor':
        controller = SensorController()
    else:
        controller = ArrowKeyController()

    try:
        config.GREEN_LED_PIN.on()
        stats = game.run(controller)
    finally:
        controller.sensor.close() if hasattr(controller, 'sensor') else None
        pg.quit()
        config.GREEN_LED_PIN.off()
        
    if data.get('phone'):
        send_sms(data['phone'], stats)

    response.content_type = 'application/json'
    return json.dumps(stats)

@route('/quit', method='POST')
def quit_game():
    config.GREEN_LED_PIN.off()
    import os
    os._exit(0)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, debug=True)
