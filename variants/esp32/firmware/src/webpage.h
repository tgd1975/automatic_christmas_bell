// The bell's web pages, each PAGE_HEAD + a body. BELLPAGE: status and time to ding, start, pause, stop and the
// timer – it polls api/status once a second and counts down in between; the commands are POSTs to api/start,
// api/pause, api/stop and api/timer (s=…). SETUPPAGE: the home network, in the setup hotspot; SAVEDPAGE: its answer.
#pragma once

const char PAGE_HEAD[] = R"html(<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weihnachtsglocke</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: system-ui, sans-serif; max-width: 26em; margin: 0 auto; padding: 1em; text-align: center; }
  #state { font-size: 1.3em; }
  #time { font-size: 4em; font-variant-numeric: tabular-nums; margin: 0.1em 0; }
  button { font-size: 1.1em; padding: 0.6em 1em; margin: 0.25em; min-width: 6em; }
  input { font-size: 1.1em; width: 4em; text-align: right; }
  .wide { width: 100%; box-sizing: border-box; text-align: left; padding: 0.4em; }
  .note { opacity: 0.7; font-size: 0.9em; }
</style>
</head>
<body>
<h1>Weihnachtsglocke</h1>
)html";

const char BELLPAGE[] = R"html(<div id="state">…</div>
<div id="time">-:--</div>
<div class="note" id="sub"></div>
<p>
  <button id="start">Start</button>
  <button id="pause">Pause</button>
  <button id="stop">Stopp</button>
</p>
<form id="timer">
  <p>Timer
    <input id="min" type="number" min="0" max="1440" inputmode="numeric"> min
    <input id="sec" type="number" min="0" max="59" inputmode="numeric"> s
    <button type="submit">Setzen</button>
  </p>
  <p class="note">10 s bis 24 h, gilt ab dem nächsten Start</p>
</form>
<p class="note" id="msg"></p>
<script>
const NAMES = {idle: 'Bereit', countdown: 'Countdown läuft', warning: 'Gleich läutet es', paused: 'Pausiert',
               ringing: 'Es läutet'};
const $ = id => document.getElementById(id);
let status = null, received = 0, edited = false;

function clock(ms) {
  let s = Math.ceil(ms / 1000);
  const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60);
  s %= 60;
  return (h ? h + ':' + String(m).padStart(2, '0') : m) + ':' + String(s).padStart(2, '0');
}

function show() {
  if (!status) return;
  const st = status.state;
  let ms = status.remaining_ms;
  if (st === 'countdown' || st === 'warning') ms = Math.max(0, ms - (Date.now() - received));
  $('state').textContent = NAMES[st] || st;
  $('time').textContent = clock(st === 'idle' ? status.timer_s * 1000 : ms);
  $('sub').textContent = st === 'idle' ? 'Timer' : 'bis zum Läuten';
  $('start').textContent = st === 'paused' ? 'Weiter' : 'Start';
  $('pause').disabled = !(st === 'countdown' || st === 'warning');
  $('stop').disabled = st === 'idle';
  if (!edited) {
    $('min').value = Math.floor(status.timer_s / 60);
    $('sec').value = status.timer_s % 60;
  }
}

function take(r) {
  if (!r.ok) {
    $('msg').textContent = 'Abgelehnt (' + r.status + ')';
    return;
  }
  return r.json().then(s => {
    status = s;
    received = Date.now();
    $('msg').textContent = '';
    show();
  });
}

function fail() { $('msg').textContent = 'Keine Verbindung zur Glocke'; }
function poll() { fetch('api/status').then(take).catch(fail); }
function send(cmd, body) { fetch('api/' + cmd, {method: 'POST', body}).then(take).catch(fail); }

$('start').onclick = () => send('start');
$('pause').onclick = () => send('pause');
$('stop').onclick = () => send('stop');
$('min').oninput = $('sec').oninput = () => { edited = true; };
$('timer').onsubmit = e => {
  e.preventDefault();
  const s = (parseInt($('min').value) || 0) * 60 + (parseInt($('sec').value) || 0);
  if (s < 10 || s > 86400) {
    $('msg').textContent = 'Timer: 10 s bis 24 h';
    return;
  }
  edited = false;
  send('timer', new URLSearchParams({s}));
};

poll();
setInterval(poll, 1000);
setInterval(show, 200);
</script>
</body>
</html>
)html";

const char SETUPPAGE[] = R"html(<p>WLAN einrichten: Die Glocke verbindet sich mit eurem WLAN. Danach ist sie unter
<b>http://glocke.local</b> erreichbar – oder unter der Adresse auf ihrem Display.</p>
<form method="post" action="/setup">
  <p><input class="wide" id="ssid" name="ssid" maxlength="32" placeholder="Netzwerk" required autocomplete="off"></p>
  <div id="nets" class="note">Suche Netzwerke …</div>
  <p><input class="wide" id="pass" name="pass" type="password" maxlength="63" placeholder="Passwort"
            autocomplete="off"></p>
  <p class="note"><label><input type="checkbox" id="show" style="width: auto"> Passwort zeigen</label></p>
  <p><button type="submit">Speichern und verbinden</button></p>
</form>
<p><button id="rescan" type="button">Netzwerke neu suchen</button></p>
<p class="note"><a href="/glocke">Glocke über den Hotspot steuern</a></p>
<script>
const $ = id => document.getElementById(id);
$('show').onchange = () => { $('pass').type = $('show').checked ? 'text' : 'password'; };

function nets() {
  fetch('/api/networks').then(r => r.json()).then(d => {
    const box = $('nets');
    box.textContent = d.scanning ? 'Suche Netzwerke …' : d.networks.length ? '' : 'Kein Netzwerk gefunden';
    const seen = new Set();
    d.networks.forEach(n => {
      if (!n.ssid || seen.has(n.ssid)) return;
      seen.add(n.ssid);
      const b = document.createElement('button');
      b.type = 'button';
      b.textContent = n.ssid;
      b.onclick = () => { $('ssid').value = n.ssid; $('pass').focus(); };
      box.appendChild(b);
    });
    if (d.scanning) setTimeout(nets, 1500);
  }).catch(() => { $('nets').textContent = 'Keine Verbindung zur Glocke'; });
}

$('rescan').onclick = () => {
  $('nets').textContent = 'Suche Netzwerke …';
  fetch('/api/scan', {method: 'POST'}).then(() => setTimeout(nets, 1500));
};
nets();
</script>
</body>
</html>
)html";

const char SAVEDPAGE[] = R"html(<p><b>Gespeichert.</b></p>
<p>Die Glocke schließt jetzt ihren Hotspot und verbindet sich mit eurem WLAN. Ihr Display zeigt danach die Adresse –
meist <b>http://glocke.local</b>.</p>
<p>Klappt die Verbindung nicht, öffnet sie den Hotspot nach 30 Sekunden wieder.</p>
</body>
</html>
)html";
