const http = require('node:http');
let requests = 0;
const server = http.createServer((req, res) => {
  if (req.url === '/metrics') {
    res.writeHead(200, {'Content-Type': 'text/plain; version=0.0.4'});
    return res.end('# HELP demo_requests_total Non-metrics HTTP requests.\n# TYPE demo_requests_total counter\ndemo_requests_total ' + requests + '\n');
  }
  requests++;
  const healthy = req.url === '/health' || req.url === '/';
  res.writeHead(healthy ? 200 : 404, {'Content-Type': 'application/json'});
  res.end(JSON.stringify({version: process.env.VERSION || 'lab', status: healthy ? 'ok' : 'not_found'}));
});
server.listen(Number(process.env.PORT || 8080), process.env.HOST || '0.0.0.0');
process.on('SIGTERM', () => server.close(() => process.exit(0)));
