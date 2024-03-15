const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const ipfilter = require('express-ipfilter').IpFilter;
const rateLimit = require('express-rate-limit');
const sqlInjection = require('sql-injection');
// const spiderDetector = require('express-spider-middleware');
const expressSpiderMiddleware = require('express-spider-middleware')
// const xssSanitizer = require('express-xss-sanitizer');
const xss = require('xss-clean');
require('dotenv').config();

const app = express();
const port = 5000;

// 1. IP Filter
const ipsPermitidas = ['::ffff:127.0.0.1', '::1'];
app.use(ipfilter(ipsPermitidas, { mode: 'allow' }));

// 2. Rate Limiter
// login
const loginLimiter = rateLimit({
  windowMs: Number(process.env.LOGIN_LIMITER_WINDOW_MS),
  max: Number(process.env.LOGIN_LIMITER_MAX),
  message: "Demasiadas solicitudes de inicio de sesión desde esta IP, inténtalo de nuevo después de un minuto",
  standardHeaders: true,
  legacyHeaders: false,
});

// edtir
const editLimiter = rateLimit({
  windowMs: Number(process.env.EDIT_LIMITER_WINDOW_MS),
  max: Number(process.env.EDIT_LIMITER_MAX),
  message: "Demasiadas solicitudes de edicion desde esta IP, inténtalo de nuevo después de un minuto",
  standardHeaders: true,
  legacyHeaders: false,
});

// Root
const rootLimiter = rateLimit({
  windowMs: Number(process.env.ROOT_LIMITER_WINDOW_MS),
  max: Number(process.env.ROOT_LIMITER_MAX),
  message: "Demasiadas solicitudes desde esta IP, por favor intenta de nuevo más tarde",
  standardHeaders: true,
  legacyHeaders: false,
});

// 3. SQL Injection
//app.use(sqlInjection);
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


app.use('/login', loginLimiter, botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3001', changeOrigin: true }));

// TODO POR IMPLEMENTAR
//app.use('/edit', editLimiter, botCheckerMiddleware, createProxyMiddleware({ target: 'http://localhost:3001', changeOrigin: true }));


app.get('/', rootLimiter, (req, res, next) => {
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
