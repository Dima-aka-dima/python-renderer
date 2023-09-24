import numpy as np
import renderer

RED = np.array(  [255, 0,   0  ], dtype = np.uint8)
GREEN = np.array([0,   255, 0  ], dtype = np.uint8)
BLUE = np.array( [0,   0,   255], dtype = np.uint8)
WHITE = np.array([255, 255, 255], dtype = np.uint8)
BLACK = np.array([0,   0,   0  ], dtype = np.uint8)

window = np.zeros([300, 300, 3], dtype = np.uint8)
renderer.clear(window, WHITE)

renderer.renderLine(window, np.array([10, 30]), np.array([50, 120]), RED, True)
renderer.renderLine(window, np.array([10, 25]), np.array([90, 15]), GREEN, True)
renderer.renderLine(window, np.array([40, 40]), np.array([40, 100]), BLUE, True)

renderer.renderQuad(window, np.array([10, 20, 30, 40]), BLACK)
renderer.renderFillTriag(window, np.array([100, 100]), np.array([200, 150]), np.array([150, 250]), BLUE)
renderer.renderFillQuad(window, np.array([20, 20, 100, 10]), GREEN)

texture = renderer.loadTexture("dog.jpg")
renderer.renderCopy(window, texture, None, np.array([100, 100, 180, 200]))
renderer.show(window)

