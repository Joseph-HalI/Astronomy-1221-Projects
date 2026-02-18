# Find all main sections using string methods
filenames = ['lectures/lecture07-llm-api-basics.md', 'lectures/lecture08-llm-function-tools-and-rag.md', 'lectures/lecture09-llm-rag-and-chromadb.md', 'lectures/lecture10-llm-rag-and-chromadb.md', 'lectures/lecture11-llm-rag-and-chromadb.md', 'lectures/lecture12-llm-rag-and-chromadb.md']
lecture_content = []

for fname in filenames:
    with open(fname, 'r') as f:
        lecture_content.append(f.read())

sections = []
lines = lecture_content.split('\n')  # Split into individual lines

for line in lines:
    # Check if line starts with '## ' (main section header)
    if line.startswith('## '):
        # Remove the '## ' to get just the title
        section_title = line[3:]  # Everything after '## '
        sections.append(section_title)

print(f"Found {len(sections)} main sections in Lectures:")
print()
for i, section in enumerate(sections[:8], 1):  # Show first 8
    print(f"  {i}. {section}")
if len(sections) > 8:
    print(f"  ... and {len(sections) - 8} more sections")

raise SystemExit(0)

def chunk_by_sections(text):
    """
    Split a document into chunks based on ## section headers.
    
    This function:
    1. Finds all the ## headers in the text
    2. Splits the document at these headers
    3. Keeps each section as a separate chunk
    4. Preserves the section header with its content
    """
    # Split on section headers
    # We use '\n## ' to ensure we're splitting on headers at line starts
    sections = text.split('\n## ')
    
    chunks = []
    for i, section in enumerate(sections):
        # The first section doesn't have '## ' removed (it wasn't split)
        if i == 0:
            chunk_text = section
        else:
            # Add back the '## ' that was removed during split
            chunk_text = '## ' + section
        
        # Only keep chunks with substantial content (at least 100 characters)
        if len(chunk_text.strip()) > 100:
            chunks.append({
                'text': chunk_text.strip(),
                'length': len(chunk_text),
                'chunk_id': i
            })
    
    return chunks