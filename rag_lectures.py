import numpy as np
import litellm
import os
import json
from sentence_transformers import SentenceTransformer
from glob import glob
from dotenv import load_dotenv
load_dotenv()

filenames = glob('lectures/*.md')  # create list of lecture files
lecture_content = ''

for fname in filenames: # read all lecture files and concatenate their contents
    with open(fname, 'r', encoding='utf-8') as f:
        lecture_content += f.read()

def chunk_by_sections(text): # define a function to chunk the lecture content by sections
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

embedding_model = SentenceTransformer('all-MiniLM-L6-v2') # load the embedding model

CHUNKS_FILE = 'chunks.json'
EMBEDDINGS_FILE = 'embeddings.npy'

# Check if precomputed files exist
if os.path.exists(CHUNKS_FILE) and os.path.exists(EMBEDDINGS_FILE):
    print("Loading cached chunks and embeddings...")
    with open(CHUNKS_FILE, 'r') as f:
        lecture_chunks = json.load(f)
    chunk_embeddings = np.load(EMBEDDINGS_FILE)

else:
    print("Computing chunks and embeddings for the first time...")
    lecture_chunks = chunk_by_sections(lecture_content)
    
    chunk_embeddings = []
    for chunk in lecture_chunks:
        embedding = embedding_model.encode(chunk['text'])
        chunk_embeddings.append(embedding)
    
    chunk_embeddings = np.array(chunk_embeddings)  # convert to array before saving
    
    # Save for next time
    with open(CHUNKS_FILE, 'w') as f:
        json.dump(lecture_chunks, f)
    np.save(EMBEDDINGS_FILE, chunk_embeddings)
    print("Saved chunks and embeddings to disk!")

def search_chunks(query, top_k=3): # define a function to search the chunks
    """
    Find the most relevant chunks for a query using vectorized operations.
    
    This function:
    1. Converts the query to an embedding (384 numbers)
    2. Calculates similarity with all chunk embeddings using vectorized NumPy
    3. Returns the top-k most similar chunks
    
    Parameters:
    - query: The search question
    - top_k: How many results to return
    """
    # Convert query to embedding (same 384-dimensional space as chunks)
    query_embedding = embedding_model.encode(query)
    
    # Vectorized similarity calculation - much faster than a loop!
    # Convert list of embeddings to NumPy array for vectorized operations
    chunk_matrix = np.array(chunk_embeddings)
    
    # Calculate dot products with all chunks at once
    similarities = np.dot(chunk_matrix, query_embedding)
    
    # Find the indices of top-k highest similarities
    # argsort() returns indices that would sort the array
    # [-top_k:] takes the last k elements (highest values)
    # [::-1] reverses to get descending order
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # Return the top chunks with their similarities
    results = []
    for idx in top_indices:
        results.append({
            'chunk': lecture_chunks[idx],
            'similarity': similarities[idx]
        })
    
    return results

def rag_answer(question, max_chunks=2): # define a function to answer questions using RAG
    """
    Answer a question using RAG (Retrieval Augmented Generation).
    
    Improved version that doesn't cut off mid-sentence!
    
    The three RAG steps:
    1. RETRIEVAL: Find relevant chunks from course materials
    2. AUGMENTATION: Add those chunks to the prompt
    3. GENERATION: Get Claude to answer using the retrieved content
    """
    print(f"Searching for content related to: '{question}'")
    
    # Step 1: Retrieve relevant chunks
    results = search_chunks(question, top_k=max_chunks)
    
    # Check if we found relevant content
    if results[0]['similarity'] < 0.2:
        return "No relevant content found in course materials for this question."
    
    print(f"Found {len(results)} relevant sections (similarity > 0.2)")
    
    # Step 2: Augment - combine retrieved chunks 
    context_parts = []
    for i, result in enumerate(results, 1):
        # Take more content but end at a complete sentence
        chunk_text = result['chunk']['text'][:1500]  # Take up to 1500 chars
        
        # Find the last period, question mark, or exclamation point
        # to end at a complete sentence
        last_sentence_end = max(
            chunk_text.rfind('.'),
            chunk_text.rfind('?'),
            chunk_text.rfind('!')
        )
        
        if last_sentence_end > 0:
            chunk_text = chunk_text[:last_sentence_end + 1]
        
        context_parts.append(f"Section {i}:\n{chunk_text}")
    
    context = "\n\n---\n\n".join(context_parts)
    
    # Create augmented prompt with retrieved content
    augmented_prompt = f"""Based on the following course materials from the lectures, answer this question: {question}

COURSE MATERIALS:
{context}

Please provide a comprehensive answer based specifically on what the course materials say. Use the exact terminology and examples from the lecture."""
    
    # Step 3: Generate answer with model
    response = litellm.completion(
    model="openai/GPT-4.1-mini", 
    max_tokens=400,
    temperature=1,
        messages=[{"role": "user", "content": augmented_prompt}],
        api_base="https://litellmproxy.osu-ai.org",
        api_key=os.getenv("ASTRO1221_API_KEY")
    )
    
    return response.choices[0].message.content
