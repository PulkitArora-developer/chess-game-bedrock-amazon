import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ChessMove, ComputerConfiguration, StockfishQueryParams, StockfishResponse, stockfishLevels } from './models';
import { BehaviorSubject, Observable, of, switchMap } from 'rxjs';
import { Color, FENChar } from 'src/app/chess-logic/models';
import { environment } from 'environment'; // Adjust the path if needed


@Injectable({
  providedIn: 'root'
})
export class StockfishService {
  static getBestMove(curr_fen: string) {
      throw new Error("Method not implemented.");
  }
  // private readonly api: string = "https://stockfish.online/api/s/v2.php";

  private readonly api: string = "https://w15sfkqcfd.execute-api.us-west-2.amazonaws.com/prod/chess";
  private readonly apiKey: string = environment.x_api_key;


  public computerConfiguration$ = new BehaviorSubject<ComputerConfiguration>({ color: Color.Black, level: 1 });

  constructor(private http: HttpClient) { }

  private convertColumnLetterToYCoord(string: string): number {
    return string.charCodeAt(0) - "a".charCodeAt(0);
  }

  private promotedPiece(piece: string | undefined): FENChar | null {
    if (!piece) return null;
    const computerColor: Color = this.computerConfiguration$.value.color;
    if (piece === "n") return computerColor === Color.White ? FENChar.WhiteKnight : FENChar.BlackKnight;
    if (piece === "b") return computerColor === Color.White ? FENChar.WhiteBishop : FENChar.BlackBishop;
    if (piece === "r") return computerColor === Color.White ? FENChar.WhiteRook : FENChar.BlackRook;
    return computerColor === Color.White ? FENChar.WhiteQueen : FENChar.BlackQueen;
  }

  private moveFromStockfishString(move: string): ChessMove {
    const prevY: number = this.convertColumnLetterToYCoord(move[0]);
    const prevX: number = Number(move[1]) - 1;
    const newY: number = this.convertColumnLetterToYCoord(move[2]);
    const newX: number = Number(move[3]) - 1;
    const promotedPiece = this.promotedPiece(move[4]);
    // console.log(prevX, prevY, newX, newY, promotedPiece)
    return { prevX, prevY, newX, newY, promotedPiece };
  }

  public getBestMove(fen: string): Observable<ChessMove> {

    const isMoveCorrect = JSON.parse(localStorage.getItem("is_move_correct") ?? "false");
    const bad_move = localStorage.getItem("bestMove") ?? "";
    
    // console.log(isMoveCorrect, bad_move);

    let body: { fen: string; is_move_correct?: boolean; bad_move?: string };

    if (!isMoveCorrect) {
      body = {
        fen: fen,
        is_move_correct: isMoveCorrect,
        bad_move: bad_move,
      };
    } else {
      body = {
        fen: fen,
      };
    } 
    
    console.log(body,bad_move);

    return this.http.post<any>(this.api, body, {
      headers: {
        'x-api-key': this.apiKey
      }
    })
    .pipe(
      switchMap(response => {
        // console.log("--response--",response)
        const bestMove: string = response.best_move;
        localStorage.setItem("bestMove", bestMove);
        // console.log("--->", bestMove)
        return of(this.moveFromStockfishString(bestMove));
      })
    )

  }
}
