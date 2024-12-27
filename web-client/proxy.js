const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
require('dotenv').config();

const app = express();

const allowedOrigins = (process.env.ALLOWED_ORIGINS || '').split(',').map(origin => origin.trim());

app.use((req, res, next) => {
  const origin = req.headers.origin;

  if (req.method === 'OPTIONS') {
    if (allowedOrigins.includes(origin)) {
      res.header('Access-Control-Allow-Origin', origin);
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
      res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      res.status(204).end();
    } else {
      res.status(403).send('CORS not allowed');
    }
  } else {
    next();
  }
});

app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.use(
  '/',
  createProxyMiddleware({
    target: process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000',
    changeOrigin: true,
    pathRewrite: {
      '^/': '/',
    },
    onProxyRes: (proxyRes, req, res) => {
      const origin = req.headers.origin;

      if (allowedOrigins.includes(origin)) {
        res.setHeader('Access-Control-Allow-Origin', origin);
      }
    },
  })
);

const PORT = process.env.PROXY_PORT || 8010;
app.listen(PORT, () => {
  console.log(`Proxy server escuchando en el puerto ${PORT}`);
  console.log(`Allowed Origins: ${allowedOrigins}`);
});
