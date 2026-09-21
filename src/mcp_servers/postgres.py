from fastmcp import FastMCP

mcp = FastMCP("Postgres MCP server!")

@mcp.tool
def save_note():
    pass

@mcp.tool
def query_notes():
    pass

@mcp.tool
def get_schema():
    pass

