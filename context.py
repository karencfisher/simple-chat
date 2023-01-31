'''
Maintain context buffer.

There are two sections:

PRETEXT: a description of the chatbot
CONTEXT: the current conversation

The maximum length of the buffer is 2048 tokens. When it reaches 
that limit, earlier tokens of the CONTEXT is truncated. The PRETEXT 
is not changed

The number of tokens is obtained using the tiktoken module. Basically,
we tokenize the buffer, get the number of tokens, truncates the
CONTEXT portion of it, and changes back to text.

'''
import tiktoken as tt


class Context:
    def __init__(self, pretext='', max_tokens=2048):
        self.__context = ''

        # Store pretext and it's length in tokens
        self.__encoder = tt.get_encoding('p50k_base')
        self.__pretext = pretext + '\n'
        pretext_enc = self.__encoder.encode(pretext)

        # Store maximum number of tokens in the context
        self.__max_context = max_tokens - len(pretext_enc)

    def get_prompt(self):
        '''
        Manage the context capacity as well as returning the 
        combined pretext and context
        '''
        # encode the context, and truncate early portion as needed
        # to keep within limit
        encoded = self.__encoder.encode(self.__context)
        trunc = encoded[-self.__max_context:]

        # translate back to text
        decoded = [self.__encoder.decode_single_token_bytes(token) 
                   for token in trunc]
        self.__context = ''.join([token.decode() for token in decoded])

        # return concatenated pretext and context
        return self.__pretext + self.__context

    def __add__(self, text):
        '''
        Add text to context

        Input: new text
        '''
        if len(text) > 0:
            self.__context += text + '\n'

