import keras
import numpy as np
import DBGame

model = keras.models.load_model("DB_model", compile = True)
state = DBGame.State().nextState(((2, 1), (3, 1))).toVector()
arr = np.array([state])

print(arr.shape)

pred = model.predict(arr)
print(pred)