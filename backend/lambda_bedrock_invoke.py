import json
import boto3
import traceback
import os

MODEL_ID = os.environ.get("MODEL_ID", "anthropic.claude-3-5-sonnet-20241022-v2:0")
BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-west-2")

ROLE_ARN = "arn:aws:iam::391897533456:role/Bedrock-access"
SESSION_NAME = "MySessionName"


def fen_to_2d_board(fen):
    """
    Converts a FEN string into a 2D board representation.

    Parameters:
        fen (str): The FEN string representing the chess position.

    Returns:
        list: A 2D list where each sublist represents a row on the chessboard.
              Empty squares are represented by '.'.
    """
    board = []
    # Extract only the board layout part of the FEN
    fen_board = fen.split(' ')[0]

    for row in fen_board.split('/'):
        board_row = []
        for char in row:
            if char.isdigit():
                # Convert empty squares to '.'
                board_row.extend(['.' for _ in range(int(char))])
            else:
                # Add piece characters directly
                board_row.append(char)
        board.append(board_row)

    return board


def assume_role_and_get_keys(role_arn, session_name):
    try:
        # Create an STS client
        sts_client = boto3.client('sts')

        # Assume the role
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name
        )

        # Extract and return the credentials
        credentials = response['Credentials']
        access_key = credentials['AccessKeyId']
        secret_key = credentials['SecretAccessKey']
        session_token = credentials['SessionToken']

        print("Assumed Role Credentials:")
        print(f"AWS_ACCESS_KEY_ID: {access_key}")
        print(f"AWS_SECRET_ACCESS_KEY: {secret_key}")
        print(f"AWS_SESSION_TOKEN: {session_token}")

        return access_key, secret_key, session_token

    except Exception as e:
        print(f"Error assuming role: {e}")
        return None, None, None


def lambda_handler(event, context):
    access_key, secret_key, session_token = assume_role_and_get_keys(ROLE_ARN, SESSION_NAME)
    if access_key and secret_key:
        bedrock = boto3.client(
            service_name='bedrock-runtime',
            region_name=BEDROCK_REGION,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            aws_session_token=session_token
        )
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': "Error in assume role",
                'message': 'Failed'
            })
        }

    body = json.loads(event.get('body'))
    fen = body.get('fen', None)
    is_move_correct = body.get('is_move_correct', True)

    board_2d = ("\n".join([" ".join(row) for row in fen_to_2d_board(fen)]))

    if isinstance(is_move_correct, str):
        if is_move_correct.lower() == 'false':
            is_move_correct = False
        else:
            is_move_correct = True

    if fen is None:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': "No FEN Provided !!"})
        }

    try:

        # Get the input text from the event
        input_text = f"""
You are the greatest chessmaster in the world with deep strategic knowledge in chess. You are tasked with simulating an advanced chess engine playing as Black. Your primary role is to analyze the given chess position, provided in Forsyth-Edwards Notation (FEN), and return the optimal move for Black in Universal Chess Interface (UCI) format. Your output must strictly adhere to the rules of chess, ensuring the move is valid and logical for Black in the provided position.

### Input Information:
1. **FEN String**: The Forsyth-Edwards Notation (FEN) representing the chess position.
2. **2D Representation**: A visual breakdown of the FEN in a human-readable format.

### What is FEN?  
FEN, or Forsyth-Edwards Notation, is a standard way to describe the state of a chess game. It provides the following details in a single string:  
1. **Piece Placement**: The positions of all pieces on the chessboard, divided by rows, with each row separated by a `/`. Pieces are represented as:
   - Uppercase letters for White's pieces: `P` (pawn), `N` (knight), `B` (bishop), `R` (rook), `Q` (queen), `K` (king).
   - Lowercase letters for Black's pieces: `p` (pawn), `n` (knight), `b` (bishop), `r` (rook), `q` (queen), `k` (king).
   - Numbers indicate empty squares in a row (e.g., `3` means three empty squares).
2. **Active Color**: `w` for White to move, `b` for Black to move.
3. **Castling Availability**: Indicates if castling is possible for either side (e.g., `KQkq` means both kingside and queenside castling are available for both sides).
4. **En Passant Target Square**: Shows the square where an en passant capture is possible.
5. **Halfmove Clock**: The number of halfmoves since the last pawn move or capture (for the fifty-move rule).
6. **Fullmove Number**: The current move number, starting at 1 and incrementing after Black's turn.

    ### Example FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    This represents the starting position in chess, with White to move, both sides able to castle, no en passant available, and no moves made yet.


##Chess Rules and Guidelines:
   Follow these rules strictly to ensure all moves are valid:

   Note: 
   
   **Piece Movement Rules:**

      1)Pawn:
         -A pawn cannot move backward. It only moves forward (one square or two squares from its starting position for Black).
         -Moves forward one square if the destination is unoccupied.
         -Moves forward two squares from its starting position (2nd rank for Black).
         -Captures diagonally forward to an adjacent square occupied by an opponent's piece.
         -En Passant: A pawn can capture an opponent's pawn that has just moved two squares forward from its starting position, landing next to the capturing pawn. This move must occur immediately after the opponent's pawn advances.
         -Promotes to a queen, rook, bishop, or knight upon reaching the 1st rank.
   
      2)Knight: 
         -Moves in an "L" shape: two squares in one direction and one square perpendicular.
         -Can jump over other pieces but cannot land on a square occupied by a piece of the same color.
      
      3)Bishop: 
         -Moves any number of squares diagonally.
         -Cannot jump over other pieces.

      4)Rook:
         -Moves any number of squares horizontally or vertically.
         -Cannot jump over other pieces.
         -May participate in castling (see castling rules below).
            
      5)Queen:
         -Moves any number of squares horizontally, vertically, or diagonally.
         -Cannot jump over other pieces.
            
      6)King:
         -Moves one square in any direction.
         
         Castling: 
            -The king moves two squares toward a rook, and the rook jumps over the king. Castling is only allowed if:
            -Neither the king nor the rook has previously moved.
            -The squares between the king and the rook are unoccupied.
            -The king is not in check, does not move through a square under attack, and does not land in check.
           

   **General Rules:**

      1)Moves cannot place the Black king in check.
      2)The Black king must always have a legal move unless checkmate or stalemate occurs.
      3)A move is invalid if it:
         Does not conform to the piece's movement rules.
         Lands on a square occupied by a piece of the same color.
      4) Do not attempt to move pieces backwards or in an illegal direction (e.g., pawns cannot move backward or sideways).
      5) Verify that no pieces are cut off towards the left or right in a manner that violates chess movement rules.
      6) If a chss piece tries to move from a square it does not occupy, the move must be considered invalid.

   **Special Conditions:**

      1)Check:
         -The king is under attack by one or more opponent pieces.
         -The responding move must address the check (e.g., move the king, block the attack, or capture the attacking piece).
      
      2)Checkmate:
         -The king is in check, and there are no legal moves to escape.
      
      3)Stalemate:
         -The king is not in check, but there are no legal moves for any Black piece.

   **Game Termination:**

      - If either king is missing in the FEN, the game is over.
      - Insufficient material for checkmate (e.g., king vs. king, king vs. king and bishop, etc.) results in a draw.

   **Validation Requirements:**

      - Validate that the suggested move conforms to the FEN-provided board state.
      - Ensure that all moves follow the above rules, particularly pawn movement, castling, and check conditions.


   **Evaluation Metrics:*

      - Provide a numerical evaluation of the position for Black:
      - Negative values (e.g., -0.5): Advantage for Black.
      - Positive values (e.g., +1.0): Advantage for White.
      - Zero (0.0): Equal position.
      - Use -M1 or +M1 for forced checkmates.
      - Include the depth of analysis in plies (one ply = one move by either side).

   **Key Strategic Considerations:**

      -Ensure Black's king safety.
      -Address immediate threats, including checks and tactical opportunities.
      -Aim for central control and active piece play.


   **Pawn Promotion:**

      -If a pawn reaches the promotion rank (1st rank for Black), it must promote to either a queen, rook, bishop, or knight.
      -Highlight that promotion is mandatory and the pawn cannot remain a pawn.

   **King Safety:**

      -No move can place or leave the Black king in check. This is non-negotiable and must be validated for every candidate move.
      -Moves must account for pins, ensuring the king isn't indirectly exposed to check.


   **Edge Cases:**

      -Check for unusual but valid scenarios, such as positions where pawns are stuck or only one piece remains active.
      -Validate stalemate conditions when the king is not in check but has no legal moves, and no other Black piece can move.


   **Expected Output Format:**

      Your response must be in JSON format as shown below:

         If Black can deliver a checkmate in one move:

         {{
             "best_move": "h7h8q",
             "evaluation": "-M1",
             "depth": "1"
         }}

         If Black finds a move that improves its position after White plays:

         {{
             "best_move": "g8f6",
             "evaluation": "-0.4",
             "depth": "12"
         }}

         If White makes an aggressive move and Black finds an equalizing response:

         {{
             "best_move": "d7d5",
             "evaluation": "0.0",
             "depth": "14"
         }}

         If White threatens to deliver checkmate, and Black must respond to save the king:

         {{
             "best_move": "f7f6",
             "evaluation": "+1.5",
             "depth": "10"
         }}


         If Black finds a tactical sequence that gains material or creates threats:

         {{
             "best_move": "b4c3",
             "evaluation": "-1.0",
             "depth": "15"
         }}

         If a king is missing in the FEN string, respond with:

         {{
             "status": "game_over",
             "message": "The game is finished. The <Black/White> king is missing.",
             "evaluation": "<evaluation score>",
             "depth": "0"
         }}


   **Important Notes**
   - Legal Moves Only: Ensure all moves are valid according to chess rules.
   - Threats and Checks: Prioritize moves that address immediate threats or deliver checks.
   - Avoid Repetition: Suggest different moves in subsequent responses unless the best move remains unchanged.
   - Perspective: Evaluate all positions from Black's perspective.


   #TASK: You will be provided with a FEN after the White player's move. Your role is to analyze the position and suggest the best move for Black, following these requirements:

    1) Move Validation Steps:
       - Verify the piece belongs to Black
       - Confirm starting square contains the correct piece
       - Validate move direction is legal (e.g. pawns move downward)
       - Check destination square is empty or contains opponent's piece
       - Ensure move doesn't expose Black king to check

    2) Strategic Priorities:
       - Evaluate immediate tactical threats
       - Calculate forcing moves and combinations
       - Consider piece activity and development
       - Maintain pawn structure integrity
       - Ensure king safety is preserved

    3) Response Requirements:
       - Provide move in UCI format
       - Include position evaluation from Black's perspective
       - Show analysis depth in plies
       - Flag any checkmate possibilities analyze the position and return your best move for Black in UCI notation in JSON Format without explaining, describing the move:

   {{
       "best_move": "<move in UCI format>",
       "evaluation": "<evaluation score, e.g., +1.0, -0.5, 0.0, +M1>",
       "depth": "<depth in plies>"
   }}
            
#### 2D Chessboard Representation:

{board_2d}
            
HERE is the FEN after White Player Move: {fen}

        """
        
        if not is_move_correct:
            bad_move = body.get('bad_move')
            input_text += f"You suggested the move {bad_move}, but that is incorrect as it violates chess rules. Please reevaluate the position and provide the correct best move for Black."


        # Prepare the request body for Claude model
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 300,
            "top_k": 250,
            "temperature": 0.1,
            "top_p": 0.9,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": input_text
                        }
                    ]
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )

        # # Parse and return the response
        response_body = json.loads(response.get('body').read())
        assistant_response = response_body.get('content', [])

        final_response = {}
        if assistant_response and isinstance(assistant_response, list):
            output_response = assistant_response[0]
            final_response = json.loads(output_response.get('text'))

        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*' # Your URL,
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'best_move': final_response.get('best_move', ''),
                'evaluation': final_response.get('evaluation', ''),
                'depth': final_response.get('depth', ''),
                'message': 'Success'
            })
        }

    except Exception as e:
        # Log the full error traceback
        error_msg = traceback.format_exc()
        print(f"Error: {str(e)}\nTraceback: {error_msg}")

        return {
            'statusCode': 500,
            'headers': {
            'Access-Control-Allow-Origin': '*' # Your URL,
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({
                'error': str(e),
                'message': 'Failed'
            })
        }
