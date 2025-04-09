from typing import List

from ....domain.entities.language import Language

class GenerateTargetLanguageDocUseCase:
    def execute(self, target_lang:str, supported_languages: List[Language])-> str:
        return f""" 
        Supported Languages: ( **name ** → `code` *(note)*)
{"\n".join( f"        - **{lang.language}** → `{lang.code}` *({lang.note})*" for lang in  supported_languages)}
      
        **NOTE**: the output should be in
        **Target Language**: `{target_lang}`
        """
        