# LLM Cosmos Of Things (CoT) - Banking AI Assistant

## Overview

**CoT (Cosmos Of Things)** is an advanced AI banking assistant that seamlessly handles everyday banking tasks while providing personalized financial guidance through natural conversation. Using sophisticated NLP, memory systems, and contextual awareness, CoT transforms routine banking interactions into intuitive, frictionless experiences.

## Key Features

- **Natural Language Processing**: Advanced NLP to understand complex user queries
- **Memory System**: Long-term memory to recall user preferences and past interactions
- **Contextual Awareness**: Maintains conversational flow with full understanding of context
- **Chat History**: References previous conversations for personalized service
- **Intent Detection**: BERT-based model for accurate understanding of user needs
- **Hybrid RAG**: Combines retrieval and generation for accurate responses
- **Multilingual Support**: Handles multiple languages with translation capabilities
- **Multiple Interfaces**: Available via API, CLI, and web interfaces

## Technical Architecture

### Core Components
- **NLP Framework**: Advanced natural language processing
- **Memory Entity**: Long-term memory capabilities
- **Context Awareness**: Contextual conversation understanding
- **Intent Detection**: BERT-based model
- **RAG/Hybrid RAG**: Retrieval-Augmented Generation system
- **Search Capabilities**: Entity, semantic, and full-text search
- **Database**: MongoDB for document embedding and indexing

## Project Structure

```
├── ai.ziva.py                # Main entry point
├── cot/                      # Core application code
│   ├── ai/                   # AI components
│   ├── config/               # Configuration files
│   ├── packages/             # SDK and type definitions
│   ├── scripts/              # Utility scripts
│   ├── interfaces/           # User interfaces (web, telegram)
│   └── tests/                # Test suites
├── data/                     # Data files and models
├── docker-compose.yml        # Docker configuration
├── docs/                     # Documentation
└── requirements.txt          # Python dependencies
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/michaelpiper/cot.git
   cd cot
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install Node modules dependencies:
   ```bash
   npm install
   ```
4. Set up environment variables (create a `.env` file based on `.env.example`)

## Running the Application

### HTTP Interface
```bash
python ai.ziva.py -m api -p 4000
```

### CLI Interface
```bash
python ai.ziva.py -m cli
```

### Web Interface
```bash
cd cot/interfaces/web
npm run build
npm start
```

### Debug Mode (with detailed logging)
```bash
python ai.ziva.py -m debug
```

### Training Mode (train llm model for intent)
```bash
python ai.ziva.py -m train
```

## Development

### Testing
Run unit tests:
```bash
python ai.ziva.py -m unittest
```

Run integration tests:
```bash
python ai.ziva.py -m integrationtest
```

### Docker Setup
Start the application with Docker:
```bash
docker-compose up --build
```

## Configuration

Edit the configuration files in `cot/config/` to customize application behavior:
- `app_config.yaml`: Main application configuration
- `logging.yaml`: Logging settings

## Contributing

We welcome contributions! Please fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT]