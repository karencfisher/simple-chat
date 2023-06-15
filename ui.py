'''
This looks dumb for now, but this will allow space for a different UI.
E.g., a Windows app, or possibly an API or web app.
'''

class BaseUI:
    def output(self, text):
        pass

    def input(self):
        pass


class STDIO(BaseUI):
    def output(self, text):
        print(f'\rAI: {text}\n')

    def input(self):
        response =  input('Human: ')
        print('')
        return response
    
    
