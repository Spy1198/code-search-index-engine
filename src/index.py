from typing import Dict, List, Tuple

# Type Alias for clarity: (line_number, character_column_offset)
PositionMarker = Tuple[int, int]
# Postings Map Scheme: { file_path: [PositionMarkers] }
PostingsList = Dict[str, List[PositionMarker]]

class InvertedIndex:
    """In-memory inverted registry utilizing optimized nested lookup maps."""
    
    def __init__(self):
        # Master Data Store: { token_string: { file_path: [(line, offset)] } }
        self.registry: Dict[str, PostingsList] = {}

    def add_location(self, token: str, file_path: str, line: int, offset: int) -> None:
        """Inserts a precise positional coordinate into a term's postings list."""
        if token not in self.registry:
            self.registry[token] = {}
        if file_path not in self.registry[token]:
            self.registry[token][file_path] = []
            
        self.registry[token][file_path].append((line, offset))

    def remove_file(self, file_path: str) -> None:
        """Surgically purges old records of a file to prevent index duplication."""
        for token in list(self.registry.keys()):
            if file_path in self.registry[token]:
                del self.registry[token][file_path]
                
                # Clean up empty token rows to free memory footprint space
                if not self.registry[token]:
                    del self.registry[token]
