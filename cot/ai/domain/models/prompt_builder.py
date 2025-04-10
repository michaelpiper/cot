from typing import Dict, List
from ..interfaces.ai_engine import IGenAIAdapter, IAsyncGenAIAdapter
class PromptBuilder(dict):
    def __init__(
        self,
        generator: IGenAIAdapter,
        **kwargs,
    ):
        super(PromptBuilder, self).__init__(**kwargs)  
        self.generator = generator 
        self.documents = []
    def generate_text(self, user_input= []) -> str:
        return ""
    def get_system_prompt(self) -> str:
        return ""
    def load_documents  (self, documents: List[str]) -> List[Dict]:
        self.documents = documents or []
    def get_documents (self) -> List[str]:
        return self.documents or []
    
class AsyncPromptBuilder(PromptBuilder):
    def __init__(
        self,
        generator: IAsyncGenAIAdapter,
        **kwargs,
    ):
        super(AsyncPromptBuilder, self).__init__(generator,**kwargs)   
    async def generate_text(self, user_input= []) -> str:
        return ""
    async def get_system_prompt(self) -> str:
        return ""
    async def load_documents  (self, documents: List[str]) -> List[Dict]:
        self.documents = documents or []
    async def get_documents (self) -> List[str]:
        return self.documents or []