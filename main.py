from src.tokenizer import CodeTokenizer
from src.index import InvertedIndex
from src.query import QueryEngine

class TextEditorIndexEngine:
    def __init__(self):
        # Instantiate our modular components
        self.tokenizer = CodeTokenizer()
        self.index = InvertedIndex()
        self.query_engine = QueryEngine(self.index)
        self.tracked_files = {}

    def save_and_index_file(self, file_path: str, content: str) -> None:
        """Simulates saving a code file and incrementally processing its search index."""
        self.tracked_files[file_path] = content
        
        # Incremental Refresh: Erase any historical index references for this file
        self.index.remove_file(file_path)
        
        # Tokenize stream directly into database postings map structures
        for token, line, offset in self.tokenizer.tokenize(content):
            self.index.add_location(token, file_path, line, offset)

    def search(self, raw_query: str) -> None:
        """Executes project-wide workspace query routing and print displays."""
        results = self.query_engine.phrase_search(raw_query)
        
        print(f"\n🔍 Searching project workspace for phrase: '{raw_query}'")
        if not results:
            print("   No match coordinates found.")
            return

        for path, markers in results.items():
            print(f"  📂 File match found in: {path}")
            file_lines = self.tracked_files[path].splitlines()
            
            for line_num, offset in markers:
                snippet = file_lines[line_num - 1].strip()
                print(f"     ↳ [Line {line_num}, Col {offset}]:  `{snippet}`")

# --- SIMULATED USER INTERACTION SUITE ---
if __name__ == "__main__":
    # Initialize Core Application Workspace
    ide_search = TextEditorIndexEngine()

    # Create mock python code files to index
    db_service_code = """import os\n\ndef init_database_connection():\n    print("Connecting...")\n    return True"""
    auth_service_code = """from db import init_database_connection\n\ndef verify_user_session():\n    # Run verification\n    init_database_connection()"""

    # Populate our indexer engine matrix
    ide_search.save_and_index_file("services/db.py", db_service_code)
    ide_search.save_and_index_file("services/auth.py", auth_service_code)

    # Test Case 1: Exact CamelCase split component verification matching
    ide_search.search("database connection")

    # Test Case 2: Multi-Word strict adjacency validation verification
    ide_search.search("def verify_user_session")
    from src.index import InvertedIndex
    from src.query import QueryEngine
    
    class TextEditorIndexEngine:
        def __init__(self):
            # Instantiate our modular components
            self.tokenizer = CodeTokenizer()
            self.index = InvertedIndex()
            self.query_engine = QueryEngine(self.index)
            self.tracked_files = {}
    
        def save_and_index_file(self, file_path: str, content: str) -> None:
            """Simulates saving a code file and incrementally processing its search index."""
            self.tracked_files[file_path] = content
            
            # Incremental Refresh: Erase any historical index references for this file
            self.index.remove_file(file_path)
            
            # Tokenize stream directly into database postings map structures
            for token, line, offset in self.tokenizer.tokenize(content):
                self.index.add_location(token, file_path, line, offset)
    
        def search(self, raw_query: str) -> None:
            """Executes project-wide workspace query routing and print displays."""
            results = self.query_engine.phrase_search(raw_query)
            
            print(f"\n🔍 Searching project workspace for phrase: '{raw_query}'")
            if not results:
                print("   No match coordinates found.")
                return
    
            for path, markers in results.items():
                print(f"  📂 File match found in: {path}")
                file_lines = self.tracked_files[path].splitlines()
                
                for line_num, offset in markers:
                    snippet = file_lines[line_num - 1].strip()
                    print(f"     ↳ [Line {line_num}, Col {offset}]:  `{snippet}`")
    
    # --- SIMULATED USER INTERACTION SUITE ---
    if __name__ == "__main__":
        # Initialize Core Application Workspace
        ide_search = TextEditorIndexEngine()
    
        # Create mock python code files to index
        db_service_code = """import os\n\ndef init_database_connection():\n    print("Connecting...")\n    return True"""
        auth_service_code = """from db import init_database_connection\n\ndef verify_user_session():\n    # Run verification\n    init_database_connection()"""
    
        # Populate our indexer engine matrix
        ide_search.save_and_index_file("services/db.py", db_service_code)
        ide_search.save_and_index_file("services/auth.py", auth_service_code)
    
        # Test Case 1: Exact CamelCase split component verification matching
        ide_search.search("database connection")
    
        # Test Case 2: Multi-Word strict adjacency validation verification
        ide_search.search("def verify_user_session")
