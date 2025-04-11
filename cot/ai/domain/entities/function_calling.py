from dataclasses import dataclass, field
from typing import List, Optional
from ..models.chat_bubble import ChatBubble

@dataclass
class FunctionCallResult:
    context: str = field(default_factory=lambda:"")
    next_step: Optional[str] = None
    bubbles: List[ChatBubble] = field(default_factory=lambda:[])
   