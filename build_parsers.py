#!/usr/bin/env python
"""
Script to build tree-sitter language parsers.
This script downloads and compiles tree-sitter language grammars for use in the AST MCP server.
"""

import os
import subprocess
from tree_sitter import Language, Parser

# Define the path where parsers will be stored
PARSERS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ast_mcp_server/parsers")
LANGUAGES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor")

# Create directories if they don't exist
os.makedirs(PARSERS_PATH, exist_ok=True)
os.makedirs(LANGUAGES_PATH, exist_ok=True)

# Define languages to install with their repository URLs
LANGUAGES = {
    "python": "https://github.com/tree-sitter/tree-sitter-python",
    "javascript": "https://github.com/tree-sitter/tree-sitter-javascript",
    "typescript": "https://github.com/tree-sitter/tree-sitter-typescript",
    "go": "https://github.com/tree-sitter/tree-sitter-go",
    "rust": "https://github.com/tree-sitter/tree-sitter-rust",
    "c": "https://github.com/tree-sitter/tree-sitter-c",
    "cpp": "https://github.com/tree-sitter/tree-sitter-cpp",
    "java": "https://github.com/tree-sitter/tree-sitter-java"
}

def clone_repo(repo_url, dest_path):
    """Clone a Git repository."""
    if not os.path.exists(dest_path):
        print(f"Cloning {repo_url} to {dest_path}")
        subprocess.run(["git", "clone", repo_url, dest_path], check=True)
    else:
        print(f"Repository already exists at {dest_path}")
        # Optionally update the repo
        subprocess.run(["git", "-C", dest_path, "pull"], check=True)

def build_languages():
    """Build tree-sitter languages and generate the library."""
    language_repos = []

    # Clone all language repositories
    for lang, repo_url in LANGUAGES.items():
        lang_path = os.path.join(LANGUAGES_PATH, f"tree-sitter-{lang}")
        clone_repo(repo_url, lang_path)
        
        # Handle TypeScript differently as it has a separate tsx parser
        if lang == "typescript":
            language_repos.extend([
                os.path.join(lang_path, "typescript"),
                os.path.join(lang_path, "tsx")
            ])
        else:
            language_repos.append(lang_path)

    # Build the languages library
    lib_path = os.path.join(PARSERS_PATH, "languages.so")
    Language.build_library(
        lib_path,
        language_repos
    )
    
    print(f"Successfully built languages library at {lib_path}")
    return lib_path

def test_parsers(lib_path):
    """Test that the parsers work correctly."""
    # Load the languages from the library
    LANGUAGE_NAMES = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "tsx": "tsx",
        "go": "go",
        "rust": "rust",
        "c": "c",
        "cpp": "cpp",
        "java": "java"
    }

    try:
        for lang_key, lang_name in LANGUAGE_NAMES.items():
            if lang_key == "tsx":
                # TSX needs special handling
                lang = Language(lib_path, "tsx")
            else:
                lang = Language(lib_path, lang_name)
            
            parser = Parser()
            parser.set_language(lang)
            
            # Create a simple test snippet for each language
            if lang_key == "python":
                test_code = "def hello(): print('world')"
            elif lang_key in ["javascript", "typescript"]:
                test_code = "function hello() { console.log('world'); }"
            elif lang_key == "tsx":
                test_code = "const App = () => <div>Hello World</div>;"
            elif lang_key == "go":
                test_code = "func main() { fmt.Println(\"Hello World\") }"
            elif lang_key == "rust":
                test_code = "fn main() { println!(\"Hello World\"); }"
            elif lang_key in ["c", "cpp"]:
                test_code = "int main() { printf(\"Hello World\\n\"); return 0; }"
            elif lang_key == "java":
                test_code = "class Main { public static void main(String[] args) { System.out.println(\"Hello World\"); } }"
            
            # Parse the code and get the AST
            tree = parser.parse(bytes(test_code, "utf8"))
            root_node = tree.root_node
            
            print(f"Successfully tested {lang_key} parser")
            print(f"  Syntax tree: {root_node.sexp()}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error testing parsers: {e}")
        return False

    return True

if __name__ == "__main__":
    try:
        lib_path = build_languages()
        test_parsers(lib_path)
        print("All parsers built and tested successfully!")
    except Exception as e:
        print(f"Error building parsers: {e}")
