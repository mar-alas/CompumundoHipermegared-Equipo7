const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const ipfilter = require('express-ipfilter').IpFilter;
const rateLimit = require('express-rate-limit');
const sqlInjection = require('sql-injection');
const expressSpiderMiddleware = require('express-spider-middleware')
const attackDetection = require('xss-attack-detection');
const xss_detect = new attackDetection.xssAttackDetection();
require('dotenv').config();

const app = express();
const port = 5000;
// app.use(express.json()); 

// 1. IP Filter
// const ipsPermitidas = ['190.165.88.228'];
const ipsPermitidas = ['::ffff:127.0.0.1', '::1'];
app.use(ipfilter(ipsPermitidas, { mode: 'allow' }));

// 2. Rate Limiter
const loginLimiter = rateLimit({
  windowMs: Number(process.env.LOGIN_LIMITER_WINDOW_MS),
  max: Number(process.env.LOGIN_LIMITER_MAX),
  message: "Demasiadas solicitudes de inicio de sesión desde esta IP, inténtalo de nuevo después de un minuto",
  standardHeaders: true,
  legacyHeaders: false,
});

// 3. SQL Injection
// app.use(sqlInjection);

// 4. Bot Detector
app.use(expressSpiderMiddleware.middleware())

// 5. XSS
const xssDetectionMiddleware = (req, res, next) => {
  const { username } = req.body;
  if (xss_detect.detect(username).gist === 'malicious') {
    return res.status(400).send('Se detectó un intento de XSS Cross-Site Scripting.');
  }
  next();
};


// Validación de bot
const botCheckerMiddleware = (req, res, next) => {
  if (req.isSpider()) {
    res.status(403).send('Acceso denegado para bots');
  } else {
    next();
  }
};


app.use('/login', loginLimiter, botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3001', changeOrigin: true }));
app.use('/api/v1/users', botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3002', changeOrigin: true }));


app.get('/', (req, res, next) => {
  if (req.isSpider()) {
    res.status(403).send('Acceso denegado para Bots');
  } else {
    next();
  }
}, (req, res) => {
  res.send('API Gateway Service con protecciones y proxy está funcionando');
});




app.listen(port, () => {
  console.log(`API Gateway escuchando en http://localhost:${port}`);
});