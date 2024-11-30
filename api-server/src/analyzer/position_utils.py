import chess

class PositionUtils:
    def get_piece_locations(self, fen):
        board = chess.Board(fen)
        piece_locations = {}

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece.piece_type
                piece_color = 'White' if piece.color == chess.WHITE else 'Black'
                piece_name = chess.PIECE_NAMES[piece_type].capitalize()  # Gets piece name like 'pawn', 'knight', etc.
                square_name = chess.square_name(square)
                piece_locations[square_name] = f'{piece_color} {piece_name}'

        sorted_piece_locations = dict(sorted(piece_locations.items(), key=lambda x: (x[1].split()[0] == 'Black', x[0])))

        return sorted_piece_locations
    
    def compute_game_phase(self, fen):
        piece_values = {
            'p': 0,
            'n': 1,
            'b': 1,
            'r': 2,
            'q': 4,
            'k': 0,
            'P': 0,
            'N': 1,
            'B': 1,
            'R': 2,
            'Q': 4,
            'K': 0
        }

        parts = fen.split()
        piece_placement = parts[0]
        move_count = int(parts[5])

        total_piece_value = sum(piece_values[piece] for piece in piece_placement if piece in piece_values)
        if total_piece_value <= 9:
            return "Endgame"
        elif move_count < 15:
            return "Opening"
        else:
            return "Middlegame"