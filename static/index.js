var board = null
var game = new Chess()
var $status = $('#status')
var $fen = $('#fen')
var $pgn = $('#pgn')

function onDragStart(source, piece, position, orientation) {
  if(game.game_over())
    return false

  if((game.turn() == 'w' && piece.search(/^b/) != -1) || game.turn() == 'b') {
    return false
  }
}

async function onDrop(source, target) {
  var move = game.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  })

  // illegal move
  if(move == null)
    return 'snapback';

  updateStatus();

  const m = await getBotMove();
  game.move(m, {sloppy: true});
}

async function getBotMove()
{
  const response = await fetch(`http://0.0.0.0:8000/getMove?fen=${game.fen()}`);
  return await response.text();
}

function onSnapEnd() {
  board.position(game.fen())
}

function updateStatus() {
  var status = ''

  var moveColor = 'White'
  if(game.turn() === 'b') {
    moveColor = 'Black'
  }

  // checkmate?
  if(game.in_checkmate()) {
    status = 'Game over, ' + moveColor + ' is in checkmate.'
  }

  // draw?
  else if(game.in_draw()) {
    status = 'Game over, drawn position'
  }

  // game still on
  else {
    status = moveColor + ' to move'

    // check?
    if(game.in_check()) {
      status += ', ' + moveColor + ' is in check'
    }
  }

  $status.html(status)
  $fen.html(game.fen())
  $pgn.html(game.pgn())
}

var config = {
  draggable: true,
  position: 'start',
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd
}

board = Chessboard('myBoard', config)
updateStatus()
