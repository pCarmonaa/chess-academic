import re

from position_utils import PositionUtils

class KingSafetyAnalyzer:
    def __init__(self):
        self.position_utils = PositionUtils()

    def parse_king_safety(self, stockfish_analysis, fen):
        # Capture squares attacked, attacked twice, and defended on the white king's flank
        white_attacks = re.findall(
            r'White King safety[\s\S]*?Squares attacked at King flank:\s*([A-H][1-8]'
            r'(?:, [A-H][1-8])*)', stockfish_analysis
        )
        white_double_attacks = re.findall(
            r'White King safety[\s\S]*?Squares attacked twice at King flank:\s*([A-H]'
            r'[1-8](?:, [A-H][1-8])*)', stockfish_analysis
        )
        white_defended_squares = re.findall(
            r'White King safety[\s\S]*?Squares defended at King flank:\s*([A-H][1-8]'
            r'(?:, [A-H][1-8])*)', stockfish_analysis
        )

        # Capture possible checks available for white pieces
        white_bishop_checks = re.findall(
            r'White King safety[\s\S]*?Bishop checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        white_knight_checks = re.findall(
            r'White King safety[\s\S]*?Knight checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        white_rook_checks = re.findall(
            r'White King safety[\s\S]*?Rook checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        white_queen_checks = re.findall(
            r'White King safety[\s\S]*?Queen checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )

        # Capture squares attacked, attacked twice, and defended on the black king's flank
        black_attacks = re.findall(
            r'Black King safety[\s\S]*?Squares attacked at King flank:\s*([A-H][1-8]'
            r'(?:, [A-H][1-8])*)', stockfish_analysis
        )
        black_double_attacks = re.findall(
            r'Black King safety[\s\S]*?Squares attacked twice at King flank:\s*([A-H]'
            r'[1-8](?:, [A-H][1-8])*)', stockfish_analysis
        )
        black_defended_squares = re.findall(
            r'Black King safety[\s\S]*?Squares defended at King flank:\s*([A-H][1-8]'
            r'(?:, [A-H][1-8])*)', stockfish_analysis
        )

        # Capture possible checks available for black pieces
        black_bishop_checks = re.findall(
            r'Black King safety[\s\S]*?Bishop checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        black_knight_checks = re.findall(
            r'Black King safety[\s\S]*?Knight checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        black_rook_checks = re.findall(
            r'Black King safety[\s\S]*?Rook checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )
        black_queen_checks = re.findall(
            r'Black King safety[\s\S]*?Queen checks availables:\s*([A-H][1-8](?:, '
            r'[A-H][1-8])*)', stockfish_analysis
        )

        num_white_attacks = len(white_attacks[0].split(', ')) if white_attacks else 0
        num_white_double_attacks = len(white_double_attacks[0].split(', ')) if \
            white_double_attacks else 0
        num_white_defended_squares = len(white_defended_squares[0].split(', ')) if \
            white_defended_squares else 0
        num_black_attacks = len(black_attacks[0].split(', ')) if black_attacks else 0
        num_black_double_attacks = len(black_double_attacks[0].split(', ')) if \
            black_double_attacks else 0
        num_black_defended_squares = len(black_defended_squares[0].split(', ')) if \
            black_defended_squares else 0

        pieces_json = self.position_utils.get_piece_locations(fen)
        game_phase = self.position_utils.compute_game_phase(fen)

        king_safety = {
            "White King Safety": {},
            "Black King Safety": {}
        }

        if game_phase in ["Opening", "Middlegame"]:
            king_safety["White King Safety"].update({
                "King in Corner": "Yes" if self.is_king_in_corner(pieces_json, 'White') else "No",
                "Adjacent Pawn Structure": self.count_adjacent_pawns(pieces_json, 'White'),
                "Pawn Structure Intact": "Yes" if self.has_intact_pawn_structure(pieces_json, 'White') else "No",
                "Open Diagonals": self.count_open_diagonals(pieces_json, 'White'),
                "Weak Columns Nearby": self.count_weak_columns_nearby(pieces_json, 'White'),
                "IsKingColumnOpen": "Yes" if self.is_king_column_open(pieces_json, 'White') else "No",  # Nuevo criterio
            })
            king_safety["Black King Safety"].update({
                "King in Corner": "Yes" if self.is_king_in_corner(pieces_json, 'Black') else "No",
                "Adjacent Pawn Structure": self.count_adjacent_pawns(pieces_json, 'Black'),
                "Pawn Structure Intact": "Yes" if self.has_intact_pawn_structure(pieces_json, 'Black') else "No",
                "Open Diagonals": self.count_open_diagonals(pieces_json, 'Black'),
                "Weak Columns Nearby": self.count_weak_columns_nearby(pieces_json, 'Black'),
                "IsKingColumnOpen": "Yes" if self.is_king_column_open(pieces_json, 'Black') else "No",  # Nuevo criterio
            })

        king_safety["White King Safety"].update({
            "Attacked Squares": num_white_attacks,
            "Double Attacked Squares": num_white_double_attacks,
            "Defended Squares": num_white_defended_squares,
            "Bishop Checks": white_bishop_checks[0] if white_bishop_checks else "None",
            "Knight Checks": white_knight_checks[0] if white_knight_checks else "None",
            "Rook Checks": white_rook_checks[0] if white_rook_checks else "None",
            "Queen Checks": white_queen_checks[0] if white_queen_checks else "None",
        })

        king_safety["Black King Safety"].update({
            "Attacked Squares": num_black_attacks,
            "Double Attacked Squares": num_black_double_attacks,
            "Defended Squares": num_black_defended_squares,
            "Bishop Checks": black_bishop_checks[0] if black_bishop_checks else "None",
            "Knight Checks": black_knight_checks[0] if black_knight_checks else "None",
            "Rook Checks": black_rook_checks[0] if black_rook_checks else "None",
            "Queen Checks": black_queen_checks[0] if black_queen_checks else "None",
        })

        return king_safety

    def get_piece_positions(self, pieces_json, piece_type):
        return [pos for pos, piece in pieces_json.items() if piece == piece_type]

    def get_king_position(self, pieces_json, color):
        return next(pos for pos, piece in pieces_json.items() if piece == f"{color} King")

    def get_adjacent_columns(self, col):
        possible_columns = [chr(ord(col) - 1), col, chr(ord(col) + 1)]
        return [c for c in possible_columns if 'a' <= c <= 'h']

    def is_in_set(self, position, position_set):
        return position in position_set

    def get_diagonal_positions_limited(self, position, direction, depth, board_size=8):
        col, row = position[0], int(position[1])
        col_delta, row_delta = direction
        diagonal = []

        for _ in range(depth):
            col = chr(ord(col) + col_delta)
            row += row_delta
            if 'a' <= col <= 'h' and 1 <= row <= board_size:
                diagonal.append(f"{col}{row}")
            else:
                break
        return diagonal

    def is_king_in_corner(self, pieces_json, color):
        corners = {
            "White": {"a1", "b1", "c1", "a2", "b2", "h1", "g1", "f1", "h2", "g2"},
            "Black": {"a8", "b8", "c8", "a7", "b7", "h8", "g8", "f8", "h7", "g7"}
        }
        king_pos = self.get_king_position(pieces_json, color)
        return self.is_in_set(king_pos, corners[color])

    def count_adjacent_pawns(self, pieces_json, color, max_distance=2):
        king_pos = self.get_king_position(pieces_json, color)
        king_col, king_row = king_pos[0], int(king_pos[1])
        
        pawn_positions = self.get_piece_positions(pieces_json, f"{color} Pawn")
        
        adjacent_columns = self.get_adjacent_columns(king_col)
        
        adjacent_pawns = 0
        for col in adjacent_columns:
            for distance in range(1, max_distance + 1):
                row = king_row + distance if color == "White" else king_row - distance
                if f"{col}{row}" in pawn_positions:
                    adjacent_pawns += 1

        return f"{adjacent_pawns}/{len(adjacent_columns)}"

    def has_intact_pawn_structure(self, pieces_json, color):
        king_pos = self.get_king_position(pieces_json, color)
        king_col, king_row = king_pos[0], int(king_pos[1])
        pawn_positions = self.get_piece_positions(pieces_json, f"{color} Pawn")
        front_row = king_row + 1 if color == "White" else king_row - 1

        adjacent_columns = self.get_adjacent_columns(king_col)
        for col in adjacent_columns:
            if f"{col}{front_row}" not in pawn_positions:
                return False
        return True

    def count_open_diagonals(self, pieces_json, color, depth=3):
        king_pos = self.get_king_position(pieces_json, color)
        diagonals = [
            self.get_diagonal_positions_limited(king_pos, direction=(-1, -1), depth=depth),
            self.get_diagonal_positions_limited(king_pos, direction=(-1, 1), depth=depth),
            self.get_diagonal_positions_limited(king_pos, direction=(1, -1), depth=depth),
            self.get_diagonal_positions_limited(king_pos, direction=(1, 1), depth=depth)
        ]
        
        pawn_positions = self.get_piece_positions(pieces_json, f"{color} Pawn")
        
        open_diagonals = 0
        for diagonal in diagonals:
            if len(diagonal) >= depth and not any(pos in pawn_positions for pos in diagonal):
                open_diagonals += 1

        return open_diagonals

    def count_weak_columns_nearby(self, pieces_json, color, depth=3):
        king_pos = self.get_king_position(pieces_json, color)
        king_col, king_row = king_pos[0], int(king_pos[1])
        
        adjacent_columns = self.get_adjacent_columns(king_col)
        
        pawn_positions = self.get_piece_positions(pieces_json, f"{color} Pawn")
        
        weak_columns = 0
        for col in adjacent_columns:
            column_is_weak = True
            for row_delta in range(depth+1):
                row = king_row + row_delta if color == "White" else king_row - row_delta
                if f"{col}{row}" in pawn_positions:
                    column_is_weak = False
                    break
            if column_is_weak:
                weak_columns += 1

        return weak_columns
    
    def is_king_column_open(self, pieces_json, color, max_distance=3):
        king_pos = self.get_king_position(pieces_json, color)
        king_col, king_row = king_pos[0], int(king_pos[1])

        pawn_positions = self.get_piece_positions(pieces_json, f"{color} Pawn")
        
        for distance in range(1, max_distance + 1):
            row = king_row + distance if color == "White" else king_row - distance
            if f"{king_col}{row}" in pawn_positions:
                return False

        return True