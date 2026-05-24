import re
from typing import Generator, Tuple

class CodeTokenizer:
    """Handles low-level code tokenization tracking sequential word order."""
    
    WORD_REGEX = re.compile(r'\w+')
    SPLIT_REGEX = re.compile(r'[a-zA-Z][a-z]*|[0-9]+')

    def tokenize(self, text: str) -> Generator[Tuple[str, int, int], None, None]:
        """
        Scans code. 
        Yields: (lowercase_token, line_number, token_sequence_index)
        """
        lines = text.splitlines()
        token_sequence_counter = 0
        
        for line_idx, line in enumerate(lines):
            line_num = line_idx + 1
            
            for match in self.WORD_REGEX.finditer(line):
                word = match.group(0)
                lower_word = word.lower()
                
                # Yield the primary token block
                yield lower_word, line_num, token_sequence_counter
                
                # Break apart compound names, but keep them on the same sequence footprint
                sub_words = self.SPLIT_REGEX.findall(word)
                if len(sub_words) > 1:
                    for sub in sub_words:
                        yield sub.lower(), line_num, token_sequence_counter
                
                # Advance sequence integer position counter
                token_sequence_counter += 1
