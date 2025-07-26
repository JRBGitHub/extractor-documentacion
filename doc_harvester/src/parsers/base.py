from typing import Protocol, List

class DocumentationParser(Protocol):
    """Protocol for documentation parsers"""
    
    def parse_section(self, html: str) -> dict:
        """Parse a documentation section"""
        ...
    
    def extract_code_examples(self, html: str) -> List[str]:
        """Extract code examples from HTML"""
        ...
    
    def get_category(self, html: str) -> str:
        """Get category from HTML content"""
        ...
