from abc import ABC, abstractmethod

class AbstractRepository(ABC):
    @abstractmethod
    def get_by_id(id: int):
        """Recupera l'oggetto con un dato id"""
        pass

    @abstractmethod
    def get_all():
        """Recupera tutte le istanze"""
        pass

    @abstractmethod
    def create(data):
        """Creare una nuova istanza"""
        pass
    
    @abstractmethod
    def delete(id: int)->bool:
        """Eliminare una istanza esistente"""
        pass

    @abstractmethod
    def update(id: int):
        pass
