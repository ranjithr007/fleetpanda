class BaseRepository:

    def __init__(self, db):
        self.db = db

    def add(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)

        return entity

    def delete(self, entity):

        self.db.delete(entity)
        self.db.commit()

    def get_by_id(self, model, id: int):
        return self.db.query(model).filter(model.id == id).first()