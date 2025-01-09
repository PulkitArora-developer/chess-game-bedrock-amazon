## How to Get FEN String from Chess Board

To get the current FEN (Forsyth–Edwards Notation) string from your chess board, you need to access the `boardAsFEN` getter from your ChessBoard instance. Here's how to do it:

1. If you're in a component that has access to the ChessBoard instance, you can directly use:
```typescript
const fenString = this.chessBoard.boardAsFEN;
```

2. If you're using the ChessBoardComponent, you can access it through the chess board service:
```typescript
// Assuming you have injected ChessBoardService
constructor(private chessBoardService: ChessBoardService) { }

// Get the FEN string
const fenString = this.chessBoardService.chessBoard.boardAsFEN;
```

The `boardAsFEN` getter will return the complete FEN string representing the current state of the chess board, including:
- Piece positions
- Active color
- Castling availability
- En passant target square
- Halfmove clock
- Fullmove number

For example, the initial chess position would return:
`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

This FEN string can then be used with your API calls to analyze or process the current chess position.