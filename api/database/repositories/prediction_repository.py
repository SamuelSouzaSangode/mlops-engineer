class PredictionRepository:
    def create(self, db, previsao):
        db.add(previsao)
        db.commit()
        db.refresh(previsao)
        return previsao