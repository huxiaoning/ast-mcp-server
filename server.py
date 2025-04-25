#!/usr/bin/env python
"""
AST/ASG Code Analysis MCP Server

This server provides code structure and semantic analysis capabilities through
the Model Context Protocol (MCP), allowing AI assistants to better understand
and reason about code.
"""

import os
import sys
import json
import hashlib
import tempfile
from mcp.server.fastmcp import FastMCP
from typing import Dict, List, Optional

# Import our tools and resources
from ast_mcp_server.tools import register_tools
from ast_mcp_server.resources import register_resources, cache_resource, get_code_hash

# Initialize the MCP server
mcp = FastMCP(
    "AstAnalyzer",
    version="0.1.0",
    description="Code structure and semantic analysis using AST/ASG"
)

# Register tools with the server
register_tools(mcp)

# Register resources with the server
register_resources(mcp)

# Add custom handlers for tool operations
# These ensure that results are cached for resource access

@mcp.tool()
def parse_and_cache(code: str, language: Optional[str] = None, filename: Optional[str] = None) -> Dict:
    """
    Parse code into an AST and cache it for resource access.
    
    This tool parses source code into an Abstract Syntax Tree and stores it
    for later retrieval as a resource. It returns both the AST data and
    a resource URI that can be used to access the data.
    
    Args:
        code: Source code to parse
        language: Programming language (optional, will be auto-detected if not provided)
        filename: Source filename (optional, helps with language detection)
        
    Returns:
        Dictionary with AST data and resource URI
    """
    from ast_mcp_server.tools import parse_code_to_ast
    
    # Generate a hash for the code
    code_hash = get_code_hash(code)
    
    # Parse the code to AST
    ast_data = parse_code_to_ast(code, language, filename)
    
    # Cache the result
    if "error" not in ast_data:
        cache_resource(code, "ast", ast_data)
        
        # Return the AST with a resource URI
        return {
            "ast": ast_data,
            "resource_uri": f"ast://{code_hash}"
        }
    else:
        return ast_data

@mcp.tool()
def generate_and_cache_asg(code: str, language: Optional[str] = None, filename: Optional[str] = None) -> Dict:
    """
    Generate an ASG from code and cache it for resource access.
    
    This tool analyzes source code to create an Abstract Semantic Graph and 
    stores it for later retrieval as a resource. It returns both the ASG data
    and a resource URI that can be used to access the data.
    
    Args:
        code: Source code to analyze
        language: Programming language (optional, will be auto-detected if not provided)
        filename: Source filename (optional, helps with language detection)
        
    Returns:
        Dictionary with ASG data and resource URI
    """
    from ast_mcp_server.tools import parse_code_to_ast, create_asg_from_ast
    
    # Generate a hash for the code
    code_hash = get_code_hash(code)
    
    # Parse to AST first
    ast_data = parse_code_to_ast(code, language, filename)
    
    if "error" in ast_data:
        return ast_data
    
    # Generate ASG
    asg_data = create_asg_from_ast(ast_data)
    
    # Cache both results
    cache_resource(code, "ast", ast_data)
    cache_resource(code, "asg", asg_data)
    
    # Return the ASG with a resource URI
    return {
        "asg": asg_data,
        "resource_uri": f"asg://{code_hash}"
    }

@mcp.tool()
def analyze_and_cache(code: str, language: Optional[str] = None, filename: Optional[str] = None) -> Dict:
    """
    Analyze code structure and cache the results for resource access.
    
    This tool analyzes source code structure and stores the results
    for later retrieval as a resource. It returns both the analysis data
    and a resource URI that can be used to access the data.
    
    Args:
        code: Source code to analyze
        language: Programming language (optional, will be auto-detected if not provided)
        filename: Source filename (optional, helps with language detection)
        
    Returns:
        Dictionary with analysis data and resource URI
    """
    from ast_mcp_server.tools import analyze_code_structure
    
    # Generate a hash for the code
    code_hash = get_code_hash(code)
    
    # Analyze the code
    analysis_data = analyze_code_structure(code, language, filename)
    
    # Cache the result
    if "error" not in analysis_data:
        cache_resource(code, "analysis", analysis_data)
        
        # Return the analysis with a resource URI
        return {
            "analysis": analysis_data,
            "resource_uri": f"analysis://{code_hash}"
        }
    else:
        return analysis_data

if __name__ == "__main__":
    # Check if tree-sitter parsers are available
    from ast_mcp_server.tools import init_parsers
    
    if not init_parsers():
        print("WARNING: Tree-sitter language parsers not found.")
        print("Run 'python build_parsers.py' to build the parsers.")
        print("Some functionality may be limited.")
    else:
        print("Tree-sitter parsers initialized successfully!")
    
    # Start the MCP server
    print("Starting AST/ASG Code Analysis MCP Server...")
    mcp.run()
