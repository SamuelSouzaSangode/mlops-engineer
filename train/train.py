import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

path = "../dados/dados_imoveis.csv"


df = pd.read_csv(path)

X = df[['area', 'quartos', 'banheiros', 'garagem']]
y = df['preco']

X_train, x_test, Y_train, y_test = train_test_split(X, 
                                                    y, 
                                                    test_size=0.2, 
                                                    random_state=42)

modelo = LinearRegression()
modelo.fit(X_train, Y_train)

score = modelo.score(x_test, y_test)
print(score)


joblib.dump(modelo, '../modelos/modelo.pkl')
print('Arquivo salvo com sucesso!!!')