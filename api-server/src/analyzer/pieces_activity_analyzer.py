import re

class PieceActivityAnalyzer:
    def parse_pieces_activity(self, stockfish_analysis):
        max_squares_controled = {
            'Bishop': 13,
            'Knight': 8,
            'Rook': 14,
            'Queen': 27
        }
        
        try:
            pieces_activity = {
                'White pieces activity': [],
                'Black pieces activity': []
            }

            # Find all blocks that describe each piece's activity
            pieces_data = re.findall(
                r'(\w+ \w+ of square \w\d[\s\S]*?(?=\n\w+ \w+ of square|\n\n|\Z))',
                stockfish_analysis
            )

            for piece_data in pieces_data:
                # Identify the type of piece and its position
                piece_type = re.findall(
                    r'(\w+ \w+) of square (\w\d)',
                    piece_data
                )
                if not piece_type:
                    continue
                
                piece_name, piece_position = piece_type[0]
                piece_info = []

                # Extract the number of squares controlled
                controlled_squares = re.findall(
                    r'Squares controlled by the \w+: ([A-H][1-8](?:, [A-H][1-8])*)',
                    piece_data
                )
                if controlled_squares:
                    num_controlled_squares = len(
                        controlled_squares[0].split(', ')
                    )
                    potencial = max_squares_controled[piece_name.split()[1]]
                    piece_info.append(
                        f'Current controlled squares: {num_controlled_squares} of {potencial} potential '
                        f'({num_controlled_squares / potencial*100:.2f}%)')

                # Extract the number of squares the piece can move to
                moveable_squares = re.findall(
                    r'The \w+ can move to: (\d+) squares',
                    piece_data
                )
                if moveable_squares:
                    potencial = max_squares_controled[piece_name.split()[1]]
                    piece_info.append(
                        f'Current moveable squares: {moveable_squares[0]} of {potencial} potential '
                        f'({int(moveable_squares[0]) / potencial*100:.2f}%)')

                # Extract additional information for specific pieces
                if 'Bishop' in piece_name or 'Knight' in piece_name:
                    distance_from_king = re.findall(
                        r'The \w+ is (\d+) squares far from our king',
                        piece_data
                    )
                    if distance_from_king:
                        piece_info.append(
                            f'Distance from king: {distance_from_king[0]} squares'
                        )

                if 'Bishop' in piece_name:
                    x_rayed_pawns = re.findall(
                        r'Number of enemy pawns x-rayed: (\d+)',
                        piece_data
                    )
                    if x_rayed_pawns:
                        piece_info.append(f'Enemy pawns x-rayed: {x_rayed_pawns[0]}')
                    
                    long_diagonal = re.findall(
                        r'The bishop is on a long diagonal and can see both center squares\.',
                        piece_data
                    )
                    if long_diagonal:
                        piece_info.append(
                            'On long diagonal, sees both center squares'
                        )

                if 'Rook' in piece_name:
                    open_column = re.findall(
                        r'The rook is on \(semi-\)open column\.',
                        piece_data
                    )
                    if open_column:
                        piece_info.append('On (semi-)open column')

                if 'Queen' in piece_name:
                    pin_or_discover_attack = re.findall(
                        r'Exists pin in or discover attack over de queen\.',
                        piece_data
                    )
                    if pin_or_discover_attack:
                        piece_info.append('Pin or discovered attack exists')

                piece_key = f'{piece_name} of {piece_position}'
                piece_activity = {
                    'Piece': piece_key,
                    'Piece info': piece_info
                }

                if 'White' in piece_name:
                    pieces_activity['White pieces activity'].append(piece_activity)
                elif 'Black' in piece_name:
                    pieces_activity['Black pieces activity'].append(piece_activity)

            return pieces_activity
        except:
            return {}