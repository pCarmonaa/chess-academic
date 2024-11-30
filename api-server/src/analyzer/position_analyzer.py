import subprocess

from position_utils import PositionUtils
from material_analyzer import MaterialAnalyzer
from pawn_structure_analyzer import PawnStructureAnalyzer
from king_safety_analyzer import KingSafetyAnalyzer
from pieces_activity_analyzer import PieceActivityAnalyzer
from threads_analyzer import ThreadsAnalyzer
from space_analyzer import SpaceAnalyzer

class PositionAnalyzer:
    def __init__(self, stockfish_path):
        self.stockfish_path = stockfish_path

        self.position_utils = PositionUtils()
        self.material_analyzer = MaterialAnalyzer()
        self.pawn_analyzer = PawnStructureAnalyzer()
        self.king_analyzer = KingSafetyAnalyzer()
        self.activity_analyzer = PieceActivityAnalyzer()
        self.threads_analyzer = ThreadsAnalyzer()
        self.space_analyzer = SpaceAnalyzer()
        
    def is_initial_position(self, fen):
        return fen.split(' ')[0] == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

    def analyze(self, fen):
        process = subprocess.Popen(
            [self.stockfish_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        commands = f"position fen {fen}\neval\n"
        stdout, stderr = process.communicate(input=commands)

        if self.has_no_analysis(stdout):
            return ""

        if stderr:
            raise Exception(f"Error running Stockfish: {stderr}")

        try:
            stockfish_analysis = stdout.split('Begin position analysis.')[1].split('End position analysis.')[0]
        except IndexError:
            raise Exception("Error processing Stockfish output: expected traces not found in output.")

        return self.parse_evaluation(stockfish_analysis, fen)
    
    def has_no_analysis(self, stdout):
        return ("Material:" not in stdout or
            "Pawn structure:" not in stdout or
            "Pieces activity:" not in stdout or
            "King safety:" not in stdout or
            "Trheats:" not in stdout or
            "Space:" not in stdout)

    def parse_evaluation(self, stockfish_analysis, fen):
        parsed_info = {}

        parsed_info['Material'] = self.material_analyzer.parse_material(stockfish_analysis)
        parsed_info['Pawn Structure'] = self.pawn_analyzer.parse_pawn_structure(stockfish_analysis)
        parsed_info['King Safety'] = self.king_analyzer.parse_king_safety(stockfish_analysis, fen)
        parsed_info['Pieces Activity'] = self.activity_analyzer.parse_pieces_activity(stockfish_analysis)
        parsed_info['Threads'] = self.threads_analyzer.parse_threads(stockfish_analysis, parsed_info['King Safety'])
        parsed_info['Space'] = self.space_analyzer.parse_space(stockfish_analysis, parsed_info['Pieces Activity'])

        return parsed_info
    
    def get_piece_locations(self, fen):
        return self.position_utils.get_piece_locations(fen)
    
    def compute_game_phase(self, fen):
        return self.position_utils.compute_game_phase(fen)