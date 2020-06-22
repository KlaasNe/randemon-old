
let players = new Map()


module.exports = (io) => {
  io.on('connection', socket =>{
    console.log('connected')

    socket.emit('initPlayers', Array.from(players.values()))

    players.set(socket.id, {id: socket.id, x:0, y:0, dir:'s'})

    socket.broadcast.emit('addPlayer', players.get(socket.id))



    socket.on('disconnect', () => {
      socket.broadcast.emit('removePlayer', socket.id)
      players.delete(socket.id)
    })

    socket.on('updatePosition', ({x,y,dir}) => {
      players.get(socket.id).x = x
      players.get(socket.id).y = y
      players.get(socket.id).dir = dir
    })
  })
  setInterval(sendPlayerPositions, 30)

  function sendPlayerPositions() {
    if(players.size > 0) {
      io.emit('playerPositions', Array.from(players.values()))
      console.log('sending', Array.from(players.values()))
    }
  }
}

