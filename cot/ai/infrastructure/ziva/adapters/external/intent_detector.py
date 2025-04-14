from .....core.adapters.external.genai_intent_detector import GemmaGenAIIntentDetector
import os
class ZiVAIntentDetector(GemmaGenAIIntentDetector):
    def __init__(self,api_key: str,  threshold: float = 0.7) -> None:
        # Get the absolute path by navigating up 4 directories from the current file's location
        absolute_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..','..'))
        # model_path = os.path.abspath(os.path.join(absolute_path,"data","models","intent_model"))
        # tokenizer_path = model_path
        # label_mappings_path = os.path.join(model_path,"label_mappings.pkl")
        csv_path = os.path.join(absolute_path,"data", "training", "intents_with_capability_dataset.csv")
        super(ZiVAIntentDetector, self).__init__(
            api_key = api_key,
            csv_path = csv_path,
        )