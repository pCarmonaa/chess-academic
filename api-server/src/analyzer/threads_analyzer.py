import re

class ThreadsAnalyzer:
    def parse_threads(self, stockfish_analysis, king_safety_info):
        try:
            threads_info = {
                'White threads': {},
                'Black threads': {}
            }

            patterns = {
                'Enemies could be attacked by knights':
                    r'Enemies atacked by knights: ([A-H][1-8](?:, [A-H][1-8])*)',
                'Enemies could be attacked by Bishops':
                    r'Enemies atacked by Bishops: ([A-H][1-8](?:, [A-H][1-8])*)',
                'Enemies could be attacked by rooks':
                    r'Enemies atacked by rooks: ([A-H][1-8](?:, [A-H][1-8])*)',
                'Enemies could be attacked by Queens':
                    r'Enemies atacked by Queens: ([A-H][1-8](?:, [A-H][1-8])*)',
                'Enemies could be attacked by king':
                    r'Enemies atacked by king: ([A-H][1-8](?:, [A-H][1-8])*)'
            }

            white_threads_section = re.findall(
                r'Threads of White:[\s\S]*?(?=Threads of Black|Trheats|$)',
                stockfish_analysis
            )
            black_threads_section = re.findall(
                r'Threads of Black:[\s\S]*?(?=Threads of White|Trheats|$)',
                stockfish_analysis
            )

            def extract_info(section, patterns):
                info = {}
                for key, pattern in patterns.items():
                    matches = re.findall(pattern, section)
                    if matches:
                        info[key] = matches[0].split(', ')
                return info

            if white_threads_section:
                threads_info['White threads'] = extract_info(
                    white_threads_section[0], patterns
                )
            if black_threads_section:
                threads_info['Black threads'] = extract_info(
                    black_threads_section[0], patterns
                )

            if 'White King Safety' in king_safety_info:
                white_checks = []
                if king_safety_info['White King Safety'].get('Bishop Checks') and \
                        king_safety_info['White King Safety']['Bishop Checks'] != 'None':
                    white_checks.append(
                        { 'Bishop': king_safety_info['White King Safety']['Bishop Checks'].split(', ') }
                    )
                if king_safety_info['White King Safety'].get('Knight Checks') and \
                        king_safety_info['White King Safety']['Knight Checks'] != 'None':                    
                    white_checks.append(
                        { 'Knight': king_safety_info['White King Safety']['Knight Checks'].split(', ') }
                    )
                if king_safety_info['White King Safety'].get('Rook Checks') and \
                        king_safety_info['White King Safety']['Rook Checks'] != 'None':
                    white_checks.append(
                        { 'Rook': king_safety_info['White King Safety']['Rook Checks'].split(', ') }
                    )
                if king_safety_info['White King Safety'].get('Queen Checks') and \
                        king_safety_info['White King Safety']['Queen Checks'] != 'None':
                    white_checks.append(
                        { 'Queen': king_safety_info['White King Safety']['Queen Checks'].split(', ') }
                    )
                if white_checks:
                    threads_info['Black threads']['Possible checks on White King'] = \
                        white_checks

            if 'Black King Safety' in king_safety_info:
                black_checks = []
                if king_safety_info['Black King Safety'].get('Bishop Checks') and \
                        king_safety_info['Black King Safety']['Bishop Checks'] != 'None':
                    black_checks.append(
                        { 'Bishop': king_safety_info['Black King Safety']['Bishop Checks'].split(', ') }
                    )
                if king_safety_info['Black King Safety'].get('Knight Checks') and \
                        king_safety_info['Black King Safety']['Knight Checks'] != 'None':
                    black_checks.append(
                        { 'Knight': king_safety_info['Black King Safety']['Knight Checks'].split(', ') }
                    )
                if king_safety_info['Black King Safety'].get('Rook Checks') and \
                        king_safety_info['Black King Safety']['Rook Checks'] != 'None':
                    black_checks.append(
                        { 'Rook': king_safety_info['Black King Safety']['Rook Checks'].split(', ') }
                    )
                if king_safety_info['Black King Safety'].get('Queen Checks') and \
                        king_safety_info['Black King Safety']['Queen Checks'] != 'None':
                    black_checks.append(
                        { 'Queen': king_safety_info['Black King Safety']['Queen Checks'].split(', ') }
                    )
                if black_checks:
                    threads_info['White threads']['Possible checks on Black King'] = \
                        black_checks

            return threads_info
        except:
                return {}