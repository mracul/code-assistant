import WebSocket from 'ws';

const ws = new WebSocket('ws://localhost:8000/ws');

ws.on('open', function open() {
  console.log('connected');
  ws.send('Hello Server!');
});

ws.on('message', function incoming(data) {
  console.log(data);
});

export default ws;
