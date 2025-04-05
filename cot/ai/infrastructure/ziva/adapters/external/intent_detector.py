from .....core.adapters.external.intent_detector import IntentDetector
from os import path
class ZiVAIntentDetector(IntentDetector):
    def __init__(self,  threshold: float = 0.7) -> None:
        # Get the absolute path by navigating up 4 directories from the current file's location
        absolute_path = path.abspath(path.join(path.dirname(__file__), '..', '..', '..', '..', '..','..'))
        model_path = path.abspath(path.join(absolute_path,"data","models","intent_model"))
        tokenizer_path = model_path
        label_mappings_path = path.join(model_path,"label_mappings.pkl")
        super(ZiVAIntentDetector, self).__init__(
            model_path=model_path,
            label_mappings_path=label_mappings_path,
            tokenizer_path=tokenizer_path,
            threshold=threshold,
        )