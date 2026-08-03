from pathlib import Path
import joblib
from api.config.settings import settings

def load_model():
    BASE_DIR = Path(__file__).resolve().parents[2]
    model_path = BASE_DIR / 'modelos' / settings.MODEL_VERSION / 'modelo.pkl'

    if not model_path.exists():
        raise FileNotFoundError(
            f'Modelo não encontrado: {model_path}'
        )

    try:
        return joblib.load(model_path)
    except Exception as e:
        raise RuntimeError(
            f'Erro carregando modelo: {e}'
        )

modelo = load_model()