class DuplicationProcessingException(Exception):
    def __init__(self, _id):
        self.message = f'Arquivo ja foi importado e possui o id {_id}, verifique o status do processamento.'
        self._id = _id
        super().__init__(self.message)
