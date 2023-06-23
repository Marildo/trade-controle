class DuplicationProcessingException(Exception):
    def __init__(self, id):
        self.message = f'Arquivo ja foi importado e possui o id {id}, verifique o status do processamento.'
        self.id = id
        super().__init__(self.message)
