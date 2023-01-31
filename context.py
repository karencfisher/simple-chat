import tiktoken as tt


class Context:
    def __init__(self, pretext='', max_tokens=2048):
        '''
        Managing the context
        '''
        self.__context = ''
        self.__encoder = tt.get_encoding('p50k_base')
        self.__pretext = pretext + '\n'
        pretext_enc = self.__encoder.encode(pretext)
        self.__max_context = max_tokens - len(pretext_enc)

    def get_prompt(self):
        encoded = self.__encoder.encode(self.__context)
        trunc = encoded[-self.__max_context:]
        decoded = [self.__encoder.decode_single_token_bytes(token) 
                   for token in trunc]
        self.__context = ''.join([token.decode() for token in decoded])
        return self.__pretext + self.__context

    def __add__(self, text):
        if len(text) > 0:
            self.__context += text + '\n'

    
def test():
    context = Context(pretext='This is a pretense', max_tokens=20)
    print(context)
    print(context.get_prompt())

    context + "Hello world."
    print(context.get_prompt())

    context + "This is a boring conversation."
    print(context.get_prompt())

    context + "This is becoming even a more boring conversation."
    print(context.get_prompt())


if __name__ == '__main__':
    test()

