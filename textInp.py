from pygame_functions import *
import random

screenSize(800,800)

instructionLabel = makeLabel("Texto de entrada", 40, 10, 10, "blue", "Agency FB", "yellow")
showLabel(instructionLabel)

wordBox = makeTextBox(10, 80, 300, 0, "Enter text here", 0, 24)
showTextBox(wordBox)
entry = textBoxInput(wordBox)

wordLabel = makeLabel(entry, 30, random.randint(1,700), random.randint(50,700), "red")
showLabel(wordLabel)

pause(500)
hideLabel(wordLabel)

endWait()
