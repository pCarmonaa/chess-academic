import re

class PawnStructureAnalyzer:
    def parse_pawn_structure(self, stockfish_analysis):
        try:
            white_pawn_structure = stockfish_analysis.split('Pawn structure of White')[1]\
                                        .split('Pawn structure of Black')[0]
            black_pawn_structure = stockfish_analysis.split('Pawn structure of Black')[1]\
                                        .split('Pieces activity')[0]
            
            white_pawns = re.findall(r'Pawn of (\w\d+)', white_pawn_structure)
            black_pawns = re.findall(r'Pawn of (\w\d+)', black_pawn_structure)

            white_passed_pawns = self.calculate_passed_pawns(
                white_pawns, black_pawns, stockfish_analysis, is_white=True
            )
            black_passed_pawns = self.calculate_passed_pawns(
                black_pawns, white_pawns, stockfish_analysis, is_white=False
            )

            white_backward_pawns = self.extract_backward_pawns(white_pawn_structure)
            black_backward_pawns = self.extract_backward_pawns(black_pawn_structure)

            white_phalanx_pawns = self.calculate_phalanx(white_pawn_structure, 'white')
            black_phalanx_pawns = self.calculate_phalanx(black_pawn_structure, 'black')

            white_isolated_pawns = self.calculate_isolated_pawns(white_pawns)
            black_isolated_pawns = self.calculate_isolated_pawns(black_pawns)

            white_islands = self.calculate_pawn_islands(white_pawn_structure)
            black_islands = self.calculate_pawn_islands(black_pawn_structure)

            pawn_structure = {
                'White Passed Pawns': white_passed_pawns,
                'Black Passed Pawns': black_passed_pawns,
                'White Backward Pawns': white_backward_pawns,
                'Black Backward Pawns': black_backward_pawns,
                'White Isolated Pawns': white_isolated_pawns,
                'Black Isolated Pawns': black_isolated_pawns,
                'White Pawn Islands': white_islands,
                'Black Pawn Islands': black_islands,
                'White Phalanx Pawns': white_phalanx_pawns,
                'Black Phalanx Pawns': black_phalanx_pawns
            }

            return pawn_structure
        except:
            return {}

    def calculate_passed_pawns(self, own_pawns, opposing_pawns, stockfish_analysis, is_white):
        def is_passed_pawn(pawn, opposing_pawns, is_white):
            column, rank = pawn[0], int(pawn[1])
            column_number = ord(column) - ord('a')
            
            for opp_pawn in opposing_pawns:
                opp_column, opp_rank = opp_pawn[0], int(opp_pawn[1])
                opp_column_number = ord(opp_column) - ord('a')
                
                if abs(column_number - opp_column_number) <= 1:
                    if is_white:
                        if opp_rank > rank:
                            return False
                    else:
                        if opp_rank < rank:
                            return False
            return True

        def extract_passed_pawn_info(pawn, passed_pawn_section):
            passed_pawn_info = {}
            pawn_regex = fr'Passed pawn of {pawn} square:[\s\S]*?(\n\n|\Z)'
            match = re.search(pawn_regex, passed_pawn_section)
            if match:
                info = match.group(0)
                passed_pawn_info['Squares to Promotion'] = re.findall(
                    r'Is at (\d+) squares of promotion', info)
                passed_pawn_info['Enemy King Distance'] = re.findall(
                    r'The king enemy is at (\d+) squares of distance of it', info)
                passed_pawn_info['Blocked Status'] = re.findall(
                    r'(Is blocked and can not advance|Is not blocked and free to advance)', 
                    info)
            return passed_pawn_info if passed_pawn_info else None

        passed_pawns = [pawn for pawn in own_pawns if 
                        is_passed_pawn(pawn, opposing_pawns, is_white)]

        color = 'White' if is_white else 'Black'
        passed_pawn_section = re.findall(
            rf'Passed pawns of {color}:[\s\S]*?(?=Passed pawns of |$)', stockfish_analysis
        )

        passed_pawn_info = {
            pawn: extract_passed_pawn_info(pawn, passed_pawn_section[0])
            for pawn in passed_pawns if passed_pawn_section
        }

        passed_pawn_final = {
            pawn: passed_pawn_info.get(pawn, {}) for pawn in passed_pawns
        }

        return passed_pawn_final

    def extract_backward_pawns(self, pawn_structure):
        backward_pawns = re.findall(
            r'Pawn of (\w\d) square:\n(?:[^\n]*\n){1,6}\s*Is a backward pawn: true',
            pawn_structure, re.DOTALL
        )
        return backward_pawns

    def calculate_pawn_islands(self, pawn_structure):
        pawns = re.findall(r'Pawn of (\w\d+)', pawn_structure)
        pawns_by_column = {}
        for pawn in pawns:
            column = pawn[0]
            if column in pawns_by_column:
                pawns_by_column[column].append(pawn)
            else:
                pawns_by_column[column] = [pawn]
        
        sorted_columns = sorted(pawns_by_column.keys())
        islands = []
        current_island = []

        for i in range(len(sorted_columns)):
            if i == 0:
                current_island.extend(pawns_by_column[sorted_columns[i]])
            elif ord(sorted_columns[i]) == ord(sorted_columns[i - 1]) + 1:
                current_island.extend(pawns_by_column[sorted_columns[i]])
            else:
                islands.append(current_island)
                current_island = pawns_by_column[sorted_columns[i]]
        
        if current_island:
            islands.append(current_island)

        return islands

    def calculate_phalanx(self, pawn_structure, color):
        pawns = re.findall(r'Pawn of (\w\d+)', pawn_structure)

        pawns_by_row = {}
        for pawn in pawns:
            row = pawn[1]
            if (row == '2' and color == 'white') or (row == '7' and color == 'black'):
                continue

            if row in pawns_by_row:
                pawns_by_row[row].append(pawn)
            else:
                pawns_by_row[row] = [pawn]

        phalanxes = []

        for row, pawns_in_row in pawns_by_row.items():
            sorted_pawns = sorted(pawns_in_row)
            current_phalanx = [sorted_pawns[0]]

            for i in range(1, len(sorted_pawns)):
                if ord(sorted_pawns[i][0]) == ord(sorted_pawns[i - 1][0]) + 1:
                    current_phalanx.append(sorted_pawns[i])
                else:
                    if len(current_phalanx) > 1:
                        phalanxes.append(current_phalanx)
                    current_phalanx = [sorted_pawns[i]]
            
            if len(current_phalanx) > 1:
                phalanxes.append(current_phalanx)

        return phalanxes

    def calculate_isolated_pawns(self, pawns):
        isolated_pawns = []
        columns_with_pawn = [ord(pawn[0]) for pawn in pawns]
        
        for pawn in pawns:
            if ord(pawn[0])-1 not in columns_with_pawn and ord(pawn[0])+1 not in columns_with_pawn:
                isolated_pawns.append(pawn)

        return isolated_pawns