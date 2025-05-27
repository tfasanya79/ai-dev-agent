import tiktoken

class TokenCounter:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.total_tokens = 0
        self.encoding = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, messages):
        tokens = 0
        for message in messages:
            tokens += 4  # Approx overhead tokens per message in chat format
            for key, value in message.items():
                tokens += len(self.encoding.encode(value))
        tokens += 2  # Additional tokens per reply
        return tokens

    def add_tokens(self, messages):
        used = self.count_tokens(messages)
        self.total_tokens += used
        return used

    def reset(self):
        self.total_tokens = 0
