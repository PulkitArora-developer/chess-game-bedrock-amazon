# How to use getBestMove in chess-board.ts

To use the `getBestMove(fen)` method from StockfishService in chess-board.ts, follow these steps:

1. First, inject StockfishService into chess-board.ts by adding it to the constructor:

```typescript
constructor(private stockfishService: StockfishService) {
}
```

2. Then you can call getBestMove using the current board FEN:

```typescript
// Get the current board state as FEN
const currentFEN = this.boardAsFEN;

// Call getBestMove which returns an Observable<ChessMove>
this.stockfishService.getBestMove(currentFEN).subscribe(
  (bestMove: ChessMove) => {
    // Use the bestMove coordinates to make the move
    this.move(
      bestMove.prevX,
      bestMove.prevY, 
      bestMove.newX,
      bestMove.newY,
      bestMove.promotedPiece
    );
  }
);
```

Note: Make sure to also:
1. Import StockfishService at the top of chess-board.ts:
```typescript
import { StockfishService } from '../modules/computer-mode/stockfish.service';
```

2. Add StockfishService as a provider in your module if not already done.