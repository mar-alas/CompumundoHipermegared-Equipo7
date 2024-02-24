const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

// Proxy para redirigir las solicitudes al endpoint de registrar usuario
app.use('/api/v1/users', createProxyMiddleware({ target: 'http://127.0.0.1:5000', changeOrigin: true }));
app.use('/ping', createProxyMiddleware({ target: 'http://127.0.0.1:5000', changeOrigin: true }));


// Escucha en un puerto específico
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API Gateway running on port ${PORT}`);
});
