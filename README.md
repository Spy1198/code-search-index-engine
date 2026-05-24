# Custom Text Editor Inverted Index Engine

A high-performance, dependency-free text parsing and search engine built in Python. Modeled after the core mechanics of modern IDEs like VS Code, it uses a token-sequence inverted index to provide $O(1)$ phrase and sub-token queries across workspace files.

## Features
- **Syntactic Tokenization:** Safely splits camelCase and snake_case naming conventions.
- **Positional Phrase Matching:** Resolves multi-word queries based on token sequence order.
- **Incremental Updates:** Efficiently purges and rebuilds indices for modified files.
