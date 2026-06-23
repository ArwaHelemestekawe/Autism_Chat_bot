import os

class TemplateParser:

    def __init__(self, language: str=None, default_language='english'):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = "english"

        self.set_language(language)

    
    def set_language(self, language: str):
        if not language:
            self.language = self.default_language

        language_path = os.path.join(self.current_path, "locales", language)
        if os.path.exists(language_path):
            self.language = language  # if yoع find adir with langauge name 
        else:
            self.language = self.default_language


    def get(self, group: str, key: str, vars: dict={}):
        if not group or not key:
            return None
        # group = file contain the temp of sys message etc (rag.py)
        # key is each var in rag fil sys prompt etc
        # var is ex: $chunk_text" 
        group_path = os.path.join(self.current_path, "locales", self.language, f"{group}.py" )
        targeted_language = self.language
        if not os.path.exists(group_path):
            group_path = os.path.join(self.current_path, "locales", self.default_language, f"{group}.py" )
            targeted_language = self.default_language

        if not os.path.exists(group_path):
            return None
        
        # import group module while run time 
        module = __import__(f"src.stores.llm.templete.locales.{targeted_language}.{group}", fromlist=[group])

        if not module:
            return None
        
        key_attribute = getattr(module, key)
        # the document key waits text and document number so we must substitute with var
        return key_attribute.substitute(vars)