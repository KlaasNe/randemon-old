const express = require('express')
const path = require('path')
const http = require('http')
const app = express()

const httpServer = http.createServer(app)

const io = require('socket.io')(httpServer)

app.use(express.static(path.join(__dirname,'..', 'build')))

require('./controllers/socketController')(io)
let port  = process.env.port || 3001
httpServer.listen( port, () => {
  console.log('listening on port', port)
})