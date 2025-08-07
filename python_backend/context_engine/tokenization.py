import tiktoken

def get_tokenizer(encoding_name: str = "cl100k_base"):
    """
    Returns a tiktoken tokenizer for the specified encoding.
    """
    return tiktoken.get_encoding(encoding_name)

def read_file_content(file_path: str):
    """
    Reads the content of a file with error handling for encoding issues.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # If utf-8 fails, try a more lenient encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            # If all else fails, return an error message
            return f"Error reading file {file_path}: {e}"
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def count_tokens(text: str, tokenizer) -> int:
    """
    Counts the number of tokens in a given text.
    """
    return len(tokenizer.encode(text))

def chunk_content(text: str, tokenizer, max_tokens: int = 1024, overlap: int = 50):
    """
    Splits text into chunks of a maximum size with a specified overlap.
    """
    tokens = tokenizer.encode(text)

    if not tokens:
        return

    start = 0
    while start < len(tokens):
        end = start + max_tokens
        chunk_tokens = tokens[start:end]

        yield tokenizer.decode(chunk_tokens)

        if end >= len(tokens):
            break

        start += (max_tokens - overlap)
