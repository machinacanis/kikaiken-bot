class Apikey:
    """
    API密钥存储的基类
    """
    model_type: str
    model_name: str
    key: str

    def set_type(self, model_type: str):
        self.model_type = model_type

    def set_name(self, model_name: str):
        self.model_name = model_name

    def set_key(self, key: str):
        self.key = key


class DeepSeekApikey(Apikey):
    """
    Deepseek的API密钥
    """
    model_type: str = "deepseek"
    model_name: str = "deepseek-chat"
    key: str = ""

    def __init__(self, key: str):
        self.set_key(key)


class SiliconFlowApikey(Apikey):
    """
    SiliconFlow的API密钥
    """
    model_type: str = "siliconflow"
    model_name: str = ""
    key: str = ""

    def __init__(self, model: str, key: str):
        self.set_name(model)
        self.set_key(key)
