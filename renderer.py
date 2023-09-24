import numpy as np
from PIL import Image

def clear(window, color):
    window[:,:] = color

def show(window):
    image = Image.fromarray(window)
    image.save('window.png')
    
def renderPoints(window, points, colors):
    points = points.T
    window[points[0], points[1], :] = colors

def renderLine(window, p1, p2, color, antiAliasing = False):
    if(antiAliasing): renderLineAA(window, p1, p2, color)
    else: renderLineNoAA(window, p1, p2, color)
    
def renderLineNoAA(window, p1, p2, color):
    t = np.linspace(0, 1, max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1])) + 1)[:, np.newaxis]
    points = p1[np.newaxis, :]*t + (1 - t)*p2[np.newaxis, :]
    
    pointsInteger = np.round(points).astype(int).T
    
    window[pointsInteger[1], pointsInteger[0]] = color
    

def renderLineAA(window, p1, p2, color):
    EPS = 1e-6

    t = np.linspace(0, 1, max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))+1)[:, np.newaxis]
    points = (p1[np.newaxis, :]*t + (1 - t)*p2[np.newaxis, :]).T

    pointsInteger = np.round(points).astype(int)
    pointsFloor = np.floor(points + EPS).astype(int)
    pointsCeil = np.ceil(points - EPS).astype(int)

    pointsFractionFromFloor = (points - pointsFloor)[:,:,np.newaxis]
    pointsFractionFromCeil = (pointsCeil - points)[:,:,np.newaxis]
    pointsFractionFromFloorInv = 1 - pointsFractionFromFloor
    pointsFractionFromCeilInv = 1 - pointsFractionFromCeil

    color = color[np.newaxis, np.newaxis,:]

    colorFloor = pointsFractionFromFloorInv*color
    colorCeil = pointsFractionFromCeilInv*color
    
    window[pointsInteger[1], pointsFloor[0]] = colorFloor[0] + pointsFractionFromFloor[0]* window[pointsInteger[1], pointsFloor[0]]
    window[pointsInteger[1], pointsCeil[0]]  = colorCeil[0]  + pointsFractionFromCeil[0] * window[pointsInteger[1], pointsCeil[0]]
    window[pointsFloor[1], pointsInteger[0]] = colorFloor[1] + pointsFractionFromFloor[1]* window[pointsFloor[1], pointsInteger[0]]
    window[pointsCeil[1], pointsInteger[0]]  = colorCeil[1]  + pointsFractionFromCeil[1] * window[pointsCeil[1], pointsInteger[0]]

def renderQuad(window, rect, color, antiAliasing = False):
    x, y, w, h = rect
    p1, p2, p3, p4 = np.array([[x, y], [x, y+h], [x+w, y], [x+w, y+h]])

    renderLine(window, p1, p2, color, antiAliasing)
    renderLine(window, p1, p3, color, antiAliasing)
    renderLine(window, p2, p4, color, antiAliasing)
    renderLine(window, p3, p4, color, antiAliasing)

def renderFillQuad(window, rect, color):
    x, y, w, h = rect
    window[y:y+h, x:x+w] = color

def renderTriag(window, p1, p2, p3, color, antiAliasing = False):
    renderLine(window, p1, p2, color, antiAliasing)
    renderLine(window, p1, p3, color, antiAliasing)
    renderLine(window, p2, p3, color, antiAliasing)
    
def renderFillTriag(window, p1, p2, p3, color):
    ps = np.array([p1, p2, p3])
    xMin, yMin = np.min(ps, axis = 0)
    xMax, yMax = np.max(ps, axis = 0)

    subWindow = window[yMin:yMax, xMin:xMax]
    ps -= np.array([xMin, yMin])
    p1, p2, p3 = ps

    a3 = p2[0] - p1[0]
    b3 = p1[1] - p2[1]
    c3 = p1[1]*p2[0] - p2[1]*p1[0]
    
    a1 = p3[0] - p2[0]
    b1 = p2[1] - p3[1]
    c1 = p2[1]*p3[0] - p3[1]*p2[0]
    
    a2 = p1[0] - p3[0]
    b2 = p3[1] - p1[1]
    c2 = p3[1]*p1[0] - p1[1]*p3[0]
    
    # j, i = np.meshgrid(np.arange(window.shape[1]), np.arange(window.shape[0]))
    j, i = np.meshgrid(np.arange(subWindow.shape[1]), np.arange(subWindow.shape[0]))
    ind1 = (a1*i + b1*j > c1)
    ind2 = (a2*i + b2*j > c2)
    ind3 = (a3*i + b3*j > c3)


    subWindow[ind1 & ind2 & ind3] = color
    window[yMin:yMax, xMin:xMax] = subWindow
    
def loadTexture(path):
    return np.array(Image.open(path))
    
def textureResize(texture, w, h):
    h0, w0, _ = texture.shape
    i = (h0*np.arange(h)/h).astype(int)
    j = (w0*np.arange(w)/w).astype(int)
    return texture[i][:,j]

def textureCrop(texture, rect):
    x, y, w, h = rect
    return texture[y:y+h, x:x+w]

def renderCopy(window, texture, srcRect=None, dstRect=None):
    if srcRect is None: srcRect = np.array([0, 0, texture.shape[1], texture.shape[0]])
    if dstRect is None: dstRect = np.array([0, 0, window.shape[1], window.shape[0]])
    
    crop = textureCrop(texture, srcRect)
    x, y, w, h = dstRect
    cropResized = textureResize(crop, w, h)
    
    window[y:y+h, x:x+w] = cropResized
