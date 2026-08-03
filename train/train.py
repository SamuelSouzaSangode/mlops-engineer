import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

path = "../dados/dados_imoveis.csv"

#Pipeline
pipeline = Pipeline(
    steps=[
        ("scaler",StandardScaler()),
        ("model",LinearRegression())
    ]
)


#Lendo dados
df = pd.read_csv(path)

#Separando colunas entradas e targets
X = df[['area', 'quartos', 'banheiros', 'garagem']]
y = df['preco']

X_train, x_test, Y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.2, 
                                                    random_state=42)


pipeline.fit(X_train, Y_train)

score = pipeline.score(x_test, y_test)
print(score)


joblib.dump(pipeline, '../modelos/v1/modelo.pkl')
print('Arquivo salvo com sucesso!!!')