from src.index import InvertedIndex, PostingsList
from typing import Dict, List, Tuple

class QueryEngine:
    def __init__(self, index: InvertedIndex):
        self.index = index

    def _get_term_locations(self, term: str) -> PostingsList:
        return self.index.registry.get(term.lower(), {})

    def phrase_search(self, phrase: str) -> Dict[str, List[Tuple[int, int]]]:
        """Resolves multi-word queries verifying strict sequential token adjacency."""
        tokens = phrase.lower().split()
        if not tokens:
            return {}
        
        candidates = self._get_term_locations(tokens[0])
        if not candidates:
            return {}
            
        final_matches = {}

        for file_path, positions in candidates.items():
            valid_phrase_starts = []
            
            for start_line, start_seq in positions:
                is_match_broken = False
                
                # We want the next matching token to be either on the SAME token block 
                # (for composite snake/camel cases) or the immediate next sequential index (+1)
                expected_seq = start_seq
                
                for i in range(1, len(tokens)):
                    next_token = tokens[i]
                    next_token_locations = self._get_term_locations(next_token).get(file_path, [])
                    
                    # Verify if token matches expected positional index bounds
                    matched_adjacency = any(
                        l == start_line and (max(expected_seq, target_seq) - min(expected_seq, target_seq) <= 1)
                        for l, target_seq in next_token_locations
                    )
                    
                    if not matched_adjacency:
                        is_match_broken = True
                        break
                    
                    # Advance token pointer positional anchor map frame
                    for l, target_seq in next_token_locations:
                        if l == start_line and (max(expected_seq, target_seq) - min(expected_seq, target_seq) <= 1):
                            expected_seq = target_seq
                            break
                            
                if not is_match_broken:
                    # Append match coordinates to line map positions
                    if (start_line, start_seq) not in valid_phrase_starts:
                        valid_phrase_starts.append((start_line, start_seq))
            
            if valid_phrase_starts:
                final_matches[file_path] = valid_phrase_starts

        return final_matches
