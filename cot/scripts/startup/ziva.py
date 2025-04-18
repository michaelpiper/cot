import argparse
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
from cot.ai import __version__
load_dotenv(dotenv_path=".env")

def parse_args(args: Optional[list] = None):
    parser = argparse.ArgumentParser(description="Cosmos of Things Banking AI")
    
    parser.add_argument(
        "-m", "--mode",
        choices=["cli", "api", "debug", "unittest", "integrationtest", "train"],
        default="cli",
        help="Execution mode (default: cli)"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="API host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "-t", "--test",
        action="store_true",
        default=False,
        help="API test mode (default: False)"
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8000,
        help="API port (default: 8000)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    return parser.parse_args(args)
    
async def main():
    args = parse_args()
    if args.mode == "cli":
        # Start the chat CLI
        from cot.ai.entrypoints.ziva.cli import start_cli
        await start_cli()
    elif args.mode == "debug":
        from .debug import debug
        debug()
    elif args.mode == "unittest":
        import subprocess
        subprocess.run(["python","-m", "cot.scripts.startup.ziva_unittest"], cwd=os.getcwd())
    elif args.mode == "train":
        import subprocess
        if args.test:
            subprocess.run(["python","-m", "cot.scripts.data_processing.verify_intents"], cwd=os.getcwd())
        else:
            subprocess.run(["python","-m", "cot.scripts.data_processing.prepare_intents"], cwd=os.getcwd())
            subprocess.run(["python","-m", "cot.scripts.data_processing.ziva_seed_knowledge_graph"], cwd=os.getcwd())
            subprocess.run(["python","-m", "cot.scripts.data_processing.ziva_seed_document_embeddings"], cwd=os.getcwd())    
    elif args.mode == "integrationtest":
        pass
    elif args.mode == "api":
        from cot.ai.entrypoints.ziva.api import start_api
        await start_api(host=args.host, port=args.port)    
  
if __name__ == "__main__":
    asyncio.run(main())
   