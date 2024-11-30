import re

class MaterialAnalyzer:
    def parse_material(self, stockfish_analysis):
        try:
            material_info = {}

            def extract_material_section(section_name, stockfish_analysis):
                pattern = (
                    fr'{section_name}:[\s\S]*?Pawns: (\d+)[\s\S]*?Bishops: (\d+)[\s\S]*?'
                    fr'Bishops pair:(true|false)[\s\S]*?Knight: (\d+)[\s\S]*?Rooks: (\d+)[\s\S]*?'
                    fr'Queens: (\d+)'
                )
                material_section = re.findall(pattern, stockfish_analysis)
                if material_section:
                    return {
                        'Pawns': int(material_section[0][0]),
                        'Bishops': int(material_section[0][1]),
                        'Bishops pair': material_section[0][2] == 'true',
                        'Knights': int(material_section[0][3]),
                        'Rooks': int(material_section[0][4]),
                        'Queens': int(material_section[0][5])
                    }
                return None

            material_info['White material'] = extract_material_section('White matetial', stockfish_analysis)
            material_info['Black material'] = extract_material_section('Black matetial', stockfish_analysis)

            return material_info
        except:
            return {}