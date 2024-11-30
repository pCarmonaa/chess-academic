import re

class SpaceAnalyzer:
    def parse_space(self, stockfish_analysis, pieces_activity):
        try:
            white_space_section = re.findall(
                r'Space of White:[\s\S]*?Squares behind or at our pawns: '
                r'([A-H][1-8](?:, [A-H][1-8])*)', stockfish_analysis
            )
            black_space_section = re.findall(
                r'Space of Black:[\s\S]*?Squares behind or at our pawns: '
                r'([A-H][1-8](?:, [A-H][1-8])*)', stockfish_analysis
            )

            white_space_count = len(
                white_space_section[0].split(', ')
            ) if white_space_section else 0
            black_space_count = len(
                black_space_section[0].split(', ')
            ) if black_space_section else 0

            space_info = {
                'Number of squares behind or at white pawn structure': white_space_count,
                'Number of squares controlled by white pieces': self.count_total_controlled_squares(pieces_activity, 'White'),
                'Number of squares behind or at black pawn structure': black_space_count,
                'Number of squares controlled by black pieces': self.count_total_controlled_squares(pieces_activity, 'Black'),
            }

            return space_info
        except:
            return {}
    
    def count_total_controlled_squares(self, pieces_activity, color):
        total_controlled = 0

        color_key = f"{color} pieces activity"

        if color_key in pieces_activity:
            for piece in pieces_activity[color_key]:
                piece_info = " ".join(piece["Piece info"])
                match = re.search(r"Controlled squares: (\d+)", piece_info)
                if match:
                    total_controlled += int(match.group(1))
        
        return total_controlled