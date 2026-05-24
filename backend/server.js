const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST", "PATCH"]
    }
});

app.use(cors());
app.use(express.json());

// In-memory Database
let orders = [];

// HTTP API Routes
app.get('/api/orders', (req, res) => {
    res.json(orders);
});

app.post('/api/orders', (req, res) => {
    const newOrder = {
        ...req.body,
        id: req.body.id || 'ORD-' + Math.random().toString(36).substr(2, 6).toUpperCase(),
        status: req.body.status || 'Pendiente',
        date: req.body.date || new Date().toISOString()
    };
    
    orders.push(newOrder);
    
    // Broadcast to Admin panels
    io.emit('ordersUpdate', orders);
    
    res.status(201).json(newOrder);
});

app.patch('/api/orders/:id/status', (req, res) => {
    const { id } = req.params;
    const { status } = req.body;
    
    const order = orders.find(o => o.id === id);
    if (!order) return res.status(404).json({ error: 'Order not found' });
    
    order.status = status;
    
    // Broadcast to Admin and specific users (if implementing private rooms)
    io.emit('ordersUpdate', orders);
    io.emit('orderStatusChanged', order);
    
    res.json(order);
});

// Socket.IO Connections
io.on('connection', (socket) => {
    console.log(`User connected: ${socket.id}`);
    
    // Send current orders upon connection
    socket.emit('ordersUpdate', orders);
    
    socket.on('disconnect', () => {
        console.log(`User disconnected: ${socket.id}`);
    });
});

const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
    console.log(`Cosmopolita API running on http://localhost:${PORT}`);
    console.log(`Socket.IO real-time server initialized.`);
});
