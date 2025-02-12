<div align="center">
  <img width="650" alt="Screenshot 2025-01-05 at 4 45 45 PM" src="https://github.com/user-attachments/assets/7a8e38eb-9908-409b-9270-cbb2a97b8be5" />
</div>

# Grok Community XDK
A community-maintained SDK (Standard Developer Kit) for XAI Grok models
supporting usage with the Python Programming Language. This library provides
convenient access to the xAI REST API from Python 3.11+ applications, with
type definitions for all request parameters and response fields.

## Installation

```bash
pip install xai-grok
```

## Requirements

- Python 3.11 or higher
- pydantic
- requests

## Usage

```python
from xai_grok import Grok

client = Grok(
    api_key="your-api-key-here"
)

# Example: Create a chat completion
response = client.chat_completions(
    ChatRequest(
        messages=[
            {"role": "user", "content": "Tell me about AI"}
        ],
        model="model-name-here"
    )
)
print(response.choices[0].message.content)
```

## Available Endpoints

### API Key Operations
- `api_key()` - Retrieve information about the current API key

### Chat and Completion Operations
- `chat_completions(request: ChatRequest)` - Create chat completions
  - Input: ChatRequest object containing messages and model settings
  - Throws: InvalidRequestError, IncompleteRequestError

- `complete(request: CompleteRequest)` - Generate completions
  - Input: CompleteRequest object with prompt and settings
  - Throws: InvalidRequestError, IncompleteRequestError

- `completions(request: SampleRequest)` - Alternative completion endpoint
  - Input: SampleRequest object
  - Throws: InvalidRequestError, IncompleteRequestError

### Embedding Operations
- `embedding_model(model_id: str)` - Get details of a specific embedding model
  - Input: Model ID string
  - Throws: ModelNotFoundError

- `embedding_models()` - List all available embedding models

- `embeddings(request: EmbeddingRequest)` - Generate embeddings
  - Input: EmbeddingRequest object
  - Throws: InvalidRequestError, IncompleteRequestError

### Language Model Operations
- `language_model(model_id: str)` - Get details of a specific language model
  - Input: Model ID string
  - Throws: ModelNotFoundError

- `language_models()` - List all available language models

### Message Operations
- `messages(request: MessageRequest)` - Send messages
  - Input: MessageRequest object
  - Throws: InvalidRequestError, IncompleteRequestError

### Model Management
- `models()` - List all available models

- `model(model_id: str)` - Get details of a specific model
  - Input: Model ID string
  - Throws: ModelNotFoundError

### Text Operations
- `tokenize_text(request: TokenizeTextRequest)` - Tokenize input text
  - Input: TokenizeTextRequest object
  - Throws: InvalidRequestError

## Request and Response Types

All request and response types are Pydantic models, providing type safety and
validation. Refer to the schemas module for detailed type definitions.

## Base URL

The API uses `https://api.x.ai` as the base URL for all endpoints.

## Authentication

The API requires an authorized API key. Authentication-related errors are
handled by specific error types:

- `NoAPIKeyProvidedError`: Raised when no API key is provided in the Authorization header
- `InvalidAPIKeyProvidedError`: Raised when an incorrect API key is provided

To avoid these errors:
1. Obtain a valid API key from console.x.ai
2. Include it in the client initialization:
```python
client = Grok(api_key="your-api-key-here")
```

## Note on Responses

All responses are parsed into their corresponding Pydantic models, providing
type-safe access to response data. If the API response cannot be parsed into
the expected type, a `FailedToParseResponseError` will be raised.
