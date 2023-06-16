'''
Maintain context buffer for ChatGPT.

There are two sections:

PRETEXT: a description of the chatbot
CONTEXT: the current conversation

The maximum length of the buffer is 4096 tokens. We will deduct the
length of the pretext, and the maximum tokens for a response. When
queried for the current context, will will return messages from
the most recent until fitting within the difference.

'''
import tiktoken as tt


class Context:
    def __init__(self, pretext, num_response_tokens=128, max_context_tokens=4096):
        self.__max_context_tokens = max_context_tokens
        self.__num_response_tokens = num_response_tokens
        self.__context = []
        self.__pretext = []

        # get system prompt (pretext)
        self.__encoder = tt.get_encoding('p50k_base')
        self.__num_pretext_tokens = len(self.__encoder.encode(pretext))
        self.__pretext.append({'role': 'system', 'content': pretext})
        self.__max_conv = (self.__max_context_tokens - 
                           (self.__num_pretext_tokens + self.__num_response_tokens))

    def get_prompt(self):
        '''
        Manage the context capacity as well as returning the 
        combined pretext and context
        '''
        # encode the context, and truncate early portion as needed
        # to keep within limit
        n_tokens = 0
        context = []
        for indx in range(len(self.__context) - 1, -1, -1):
            n_tokens += self.__context[indx]['n_tokens']
            if n_tokens >= self.__max_conv:
                break
            context.append(self.__context[indx]['message'])

        # return concatenated pretext and context
        return self.__pretext + context[::-1]

    def add(self, role, text, provider='openai', n_tokens=None):
        '''
        Add token count, role, and content to the context

        Input: new text
        '''
        if len(text) > 0:
            # if not passed, estimate number of tokens
            if n_tokens is None or n_tokens == 0:
                n_tokens = len(self.__encoder.encode(text))

            # assemble message and add to appropriate list
            if provider in ['openai', 'gpt4all']:
                message = {'n_tokens': n_tokens, 
                        'message': {'role': role, 'content': text}}
            elif provider == 'PaLM':
                message = {'n_tokens': n_tokens, 
                        'message': {'author': role, 'content': text}}
            else:
                raise ValueError('Unknown provider')

            self.__context.append(message)

