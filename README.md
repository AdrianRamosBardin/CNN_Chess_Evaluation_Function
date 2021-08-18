# CNN_Chess_Evaluation_Function
CNN use for creating an evaluation function for chess

EN: This project is part of a large project I am currently working on, but due to the lack of time, its progress is rather slow. The larger project is a combination of neural networks (NN) which will help a Min-Max algorithm play Chess.

This part of the project involves the evaluation function of the Min-Max algorithm. In this case, we are getting the data in form of a FEN (Forsyth–Edwards Notation) string, and processing it using a chess library in python.

With the FEN string, which contains all the moves in that game we generate all the different boards which have occurred in that game.
Finally, we use Stockfish, a very powerful open-source chess engine to evaluate each one of the boards.

At this point is where the thing becomes interesting, I create CNN (Convolutional Neural Network) to learn with the provided data how to evaluate a chessboard.
I use a CNN because the data of the boards are given in a similar fashion as images, in this case, an 8x8x6 3D matrix. The 8x8 comes from the chessboard and the six from the pieces, I use one-hot encoding for vectorizing the chessboards.

DISCLAIMER: The code is commented and programed in my language (Spanish)

ES: Este proyecto es parte de un gran proyecto en el que estoy trabajando actualmente, pero debido a la falta de tiempo, su avance es bastante lento. El proyecto más grande es una combinación de redes neuronales (NN) que ayudarán a un algoritmo Min-Max a jugar al ajedrez.

Esta parte del proyecto involucra la función de evaluación del algoritmo Min-Max. En este caso, obtenemos los datos en forma de una cadena FEN (notación de Forsyth-Edwards) y los procesamos usando una biblioteca de ajedrez en Python.

Con la cadena FEN, que contiene todos los movimientos en ese juego, generamos todos los diferentes tableros que han ocurrido en ese juego.
Por último, utilizamos Stockfish, un engine de ajedrez de código abierto muy potente para evaluar cada uno de los tableros.

En este punto es donde la cosa se pone interesante, creo CNN (Convolutional Neural Network) para aprender con los datos proporcionados cómo evaluar un tablero de ajedrez.
Utilizo una CNN porque los datos de los tableros se dan de manera similar a las imágenes, en este caso, una matriz 3D de 8x8x6. El 8x8 proviene del tablero de ajedrez y el seis de las piezas, yo uso codificación one-hot para vectorizar los tableros de ajedrez.
