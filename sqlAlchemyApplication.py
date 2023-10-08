from sqlalchemy.orm import Query
from sqlalchemy import create_engine, ForeignKey, select, func
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Attributes
    id = Column(Integer, primary_key=True)
    nome = Column(String(30))
    cpf = Column(String(9))
    endereco = Column(String(20))

    conta = relationship(
        "Conta", back_populates="user"
    )

    def __repr__(self):
        return f"User(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"

class Conta(Base):
    __tablename__ = "conta"
    # Attributes
    id = Column(Integer, primary_key=True)
    tipo_conta = Column(String)
    agencia = Column(String)
    numero_conta = Column(Integer)
    saldo = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="conta")

    def __repr__(self):
        return (f"Conta(id={self.id}, tipo_conta={self.tipo_conta},"
                f"agencia={self.agencia}, saldo={self.saldo})")


# Conexão com o banco de dados
engine = create_engine('sqlite:///desafio.db', echo=True)

# Criando as classes com tabelas no banco de dados
Base.metadata.create_all(engine)

with Session(engine) as session:
    adriel = User(
        nome='adriel',
        cpf='000111222',
        endereco='fortaleza',
        conta=[Conta(tipo_conta='corrente', agencia='001', numero_conta='123', saldo=1250)],
    )

    vitoria = User(
        nome='vitoria',
        cpf='222333444',
        endereco='caucaia',
        conta=[Conta(tipo_conta='poupanca', agencia='001', numero_conta='456', saldo=250)],
    )

    session.add_all([adriel, vitoria])
    #session.commit()

    query_User = session.query(User).filter_by(nome='vitoria').first()

    for instance in session.query(User).order_by(User.id):
        print(instance.nome, instance.cpf)

with Session(engine) as session:
    for user in session.query(User):
        print(f"Nome do Usuário: {user.nome}")
        for conta in user.conta:
            print(f"Tipo de Conta: {conta.tipo_conta}")
            print(f"Saldo: {conta.saldo}")
        print("")


