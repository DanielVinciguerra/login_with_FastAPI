from _app.core.configs import settings

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates


class MembroModel(settings.DBBaseModel):
    __tablename__: str = 'membros'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    funcao: str = Column(String(100))
    imagem: str = Column(String(100)) # 150x150
    email: str = Column(String(100))
    senha: str = Column(String(400))

    @validates('funcao')
    def _valida_funcao(self, key, value):
        if value is None or value == '':
            raise ValueError('Você precisa informar uma função válida')
        
        # FAZER VERIFICACOES:
        #EXEMPLO:
        if value not in  ['inscrito','inscrito_1','administrador']:
            raise ValueError('Sua função deve envolver Python. Desculpe.')
        
        return value
