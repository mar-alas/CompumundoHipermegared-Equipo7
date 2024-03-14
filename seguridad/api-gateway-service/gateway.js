const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const ipfilter = require('express-ipfilter').IpFilter;
const rateLimiter = require('express-limiter');
const sqlInjection = require('sql-injection');
// const spiderDetector = require('express-spider-middleware');
const expressSpiderMiddleware = require('express-spider-middleware')
// const xssSanitizer = require('express-xss-sanitizer');
const xss = require('xss-clean');

const app = express();
const port = 5000;

// 1. IP Filter
const ipsPermitidas = ['::ffff:127.0.0.1', '::1'];
app.use(ipfilter(ipsPermitidas, { mode: 'allow' }));

// 2. Rate Limiter
// TODO instancia de Redis
const limiter = rateLimiter(app, {
  path: '*',
  method: 'all',
  lookup: ['connection.remoteAddress'],
  total: 150, // solicitudes por hora
  expire: 1000 * 60 * 60
});

// 3. SQL Injection
app.use(sqlInjection);

// 4. Bot Detector
app.use(expressSpiderMiddleware.middleware())


// 5. XSS
app.use(xss());


// Validación de bot
const botCheckerMiddleware = (req, res, next) => {
  if (req.isSpider()) {
    res.status(403).send('Acceso denegado para bots');
  } else {
    next();
  }
};


app.use('/login', botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3001', changeOrigin: true }));
app.use('/service2', botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3002', changeOrigin: true }));


app.get('/', (req, res) => {
  if (req.isSpider()) {
    res.status(403).send('Acceso denegado para Bots');
  } else {
    res.send('API Gateway Service con protecciones y proxy está funcionando');
  }
});



app.listen(port, () => {
  console.log(`API Gateway escuchando en http://localhost:${port}`);
});
