#A pesar del nobre de este archivo aquí se entrena la CNN también; Es decir hay data processing y CNN training

import chess.svg
from pandas import read_csv
#import numpy as np
import chess
import chess.pgn
import chess.engine
import matplotlib.pyplot as plt
import os
import statistics
import math

from tensorflow import keras
from tensorflow.keras import layers, models,initializers
from tensorflow.python.keras.backend import dropout

#Usamos funciones en otro archivo para crear los datos d entrenamiento desde las strings que sacamos del "game.csv"
from board_sequce_processor import san2list_vec
from board_sequce_processor import san2list

df = read_csv('data_chess\\games.csv')
indice = 500
#Sacamos del archivo de pandas los datos de movimientos conocidos como "moves"
data = df['moves'].tolist()[:indice]

#Aqui pasamos las strings largas con los todos los "moves" juntos a listas con con cada move separado
#A cada aaray con "moves" dentro se le llama "san"
split_data = []
for moves in data:
    split_data.append(moves.split())

#En este punto generamos un array que contiene las secuencias de boards de cada partida
#Es decir lista[0] = Una lista con las boards de la partida #0
#Dependiendo de si se una san2list o san2list_vec esas boards estaran vectorizadas o no
games_array_vec = []
for san in data:
    a = san2list_vec(san)
    games_array_vec.append(a)

games_array = []
for san in data:
    a = san2list(san)
    games_array.append(a)

#Como para entrenar a la NN de la función de evalucion no le importa la partida, juntamos todas las secuencias de boards en un solo array
#fused_sequence es un array con boards, las boards están en orden cronologico, pero eso da lo mismo
#Generamos la lista vectorizada para la NN y la no vectorizada conobjetos "Board" para poder evaluarlas con Stockfish
fused_sequence_vec = []
for sequence in games_array_vec:
    fused_sequence_vec.extend(sequence)

fused_sequence = []
for sequence1 in games_array:
    fused_sequence.extend(sequence1)
#print(fused_sequence[0])




#Creamos la lista con la puntuacion de cada tablero en el array "fused_sequence"
print("Starting Stockfish Evaluation  --> " + str(len(fused_sequence)))

#Abro la engine fuera de la función de evalucion de Stockfish por que es muchísimo más rapido abrirla solo 1 vez

engine = chess.engine.SimpleEngine.popen_uci(r"***************************************************")

def stockfish_evaluation(board, chess_engine, time_limit = 0.0001 ):
    
    result = chess_engine.analyse(board, chess.engine.Limit(time=time_limit))
    return result['score']

eval_stockfish = []

for board in fused_sequence:
    temp_result = str( stockfish_evaluation(board, engine).black() )
    #Algunas evaluciones tienen simbolos raros y hay que quitarlos por eso el "try - except"
    try:
        result = min(1, int( temp_result )/8000.0 )
        #print("OK")
    except:
        #print("Character Conflict")
        result = min(1, int( temp_result.replace("#","") )/8000.0 )

    eval_stockfish.append(result)

print(statistics.mean(eval_stockfish))
engine.close()


print("Finished data processing, starting with NN training")


#Hago un histograma para visualizar las frecuencias de las puntuaciones
print("MAX: " + str(max(eval_stockfish)) )
print("MIN: " + str(min(eval_stockfish)) )

'''
fig, axs = plt.subplots(1,2, sharey=True, tight_layout=True)
axs[0].hist(eval_stockfish, bins=50)

plt.show()
#axs[1].hist(y, bins=len(eval_stockfish))
'''

#Establecemos la estructura de la NN, Pooling no hace gran differencia por lo que he podido leer. La mayoria de CNN usadas para esto ni las llevan, ahora tiempo de entrenamiento :)

K = len(fused_sequence_vec) - 50
ker_deviation = 0.1

model = models.Sequential()

model.add(layers.Conv2D(32, 3, 3, input_shape=(8, 8, 6) ,kernel_initializer=initializers.random_normal(stddev=ker_deviation) ) )
model.add(layers.Activation('tanh'))
#model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, 3, 3, padding='same', kernel_initializer=initializers.random_normal(stddev=ker_deviation) ) )
model.add(layers.Activation('tanh'))
#model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, 3, 3, padding='same', kernel_initializer=initializers.random_normal(stddev=ker_deviation) ) )
model.add(layers.Activation('tanh'))
#model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(256, 3, 3, padding='same', kernel_initializer=initializers.random_normal(stddev=ker_deviation) ) )
model.add(layers.Activation('tanh'))
#model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Flatten())

model.add(layers.Dense(1024, kernel_initializer=initializers.random_normal(stddev=ker_deviation)))
model.add(layers.Activation('tanh'))
model.add(layers.Dropout(0.5))

model.add(layers.Dense(1, kernel_initializer=initializers.random_normal(stddev=ker_deviation)))
model.add(layers.Activation('tanh'))

model.compile(

    loss=keras.losses.mean_squared_error,
    optimizer=keras.optimizers.Adam(lr = 0.00001),
    metrics=['accuracy'],
)

earlystop = keras.callbacks.EarlyStopping(monitor='loss', min_delta=0, patience=250, verbose=0, mode='auto', baseline=None, restore_best_weights=True)

history = model.fit(
    fused_sequence_vec,
    eval_stockfish,
    epochs=15,
    callbacks = [earlystop],
    validation_data=(fused_sequence_vec[K:], eval_stockfish[K:]))

model.save("C:\\Users\\Adrián Ramos\\Desktop\\Chess AI\\Chess2Vec\\models\\board_eval2.h5")

#Resumen del modelo, con parametros entrenables
print(model.summary())

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.show()

test_loss, test_acc = model.evaluate(fused_sequence_vec[K:], eval_stockfish[K:], verbose=2)
print(test_acc)


