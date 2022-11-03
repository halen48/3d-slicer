# ===========================================================

base = "C:/Documentos/"
save_path = base+'/sliced/'

# ===========================================================

import numpy as np
import pygame
import cv2
import os


def draw_mark(img,pos,size,mark_color):
        for i in range(1,size+1):
            img[(pos[0]-i,pos[1])] = mark_color
            img[(pos[0],pos[1]+i)] = mark_color
            img[(pos[0],pos[1]-i)] = mark_color
            img[(pos[0]+i,pos[1])] = mark_color
        return img

# redimensiona a imagem para um tamanho ok
def fit_image(pixels):
    return pixels[idx_slice]

def show_pixels(pixels, seed):
    p = pixels.copy()
    p = ((255*np.moveaxis(np.array([p,p,p]),0,-1)).astype(np.uint8))
    
    for s in seed[show_mode]:
        p[s] = (default_color)
        p = draw_mark(p,s,3, (default_color))
    
    if(len(seed[show_mode]) > 1):
        p = cv2.UMat(p)
        for i in range(len(seed[show_mode])-1):
            p = cv2.line(p,seed[show_mode][i][::-1],seed[show_mode][i+1][::-1],default_color,1)
        p = cv2.line(p,seed[show_mode][-1][::-1],seed[show_mode][0][::-1],default_color,1)
        p = cv2.UMat.get(p)

    ret = pygame.surfarray.make_surface(p)
    gameDisplay.blit(ret, (0,0))

def get_area():
    for __ in range(3):            
        x_min,y_min, x_max,y_max = *seed[__][0], *seed[__][0]
        for p in seed[__]:
            x_min,y_min = min(x_min, p[0]),min(y_min, p[1])
            x_max,y_max = max(x_max, p[0]),max(y_max, p[1])
        print(seed[__])
        seed[__] = [(x_min,y_min), (x_max,y_min), (x_max,y_max), (x_min,y_max)]
        print(seed[__])
    return seed


def set_default(pixels, name):
    global gameDisplay
    window_size = pixels.shape[1:3]
    gameDisplay = pygame.display.set_mode(window_size)
    pygame.display.set_caption('%s'%name)

def rotate_axis(pixels, show_mode, direction, f_name):
    
        
    if(direction < 0):
        show_mode = (show_mode-1)%3
        if(show_mode < 0):
            show_mode = 2
        pixels = np.moveaxis(pixels,0,-1)
    else:
        show_mode = (show_mode+1)%3
        pixels = np.moveaxis(pixels,-1,0)

    idx_slice = pixels.shape[0]//2

    set_default(pixels, f_name)

    return pixels, idx_slice,show_mode

# ===========================================================

for f_name  in os.listdir(base):
    img = base+f_name
    if(os.path.isdir(img) or not '.npy' in img):
        continue

    pixels = np.load(img)

    iterative = False

    default_color = (0,255,0)


    idx_slice = pixels.shape[0]//2

    show_mode = 0
    #ajusta as imagens
    render_pixels = fit_image(pixels)

    # ===========================================================================
    pygame.init()
    gameDisplay = None

    set_default(pixels, f_name)
    done = False
    render = False
    clock = pygame.time.Clock()
    seed = {v:[] for v in range(len(pixels.shape))}

    UPDATE_FRAME = pygame.USEREVENT+1
    pygame.time.set_timer(UPDATE_FRAME, 100)
    shift = False

    while not done:

        keys=pygame.key.get_pressed()
        render = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if(event.key == 304):
                    shift = True
                if(event.key == ord('w')):
                    #transforma os pontos em um retangulo
                    seed = get_area()
                if(event.key == ord('e')):
                    pixels, idx_slice,show_mode = rotate_axis(pixels, show_mode,1, f_name)
                if(event.key == ord('q')):
                    pixels, idx_slice,show_mode = rotate_axis(pixels, show_mode,-1, f_name)
                if(event.key == ord('s')):
                    
                    while show_mode != 0:
                        pixels, idx_slice,show_mode = rotate_axis(pixels, show_mode,-1)

                    #transforma os pontos em um retangulo
                    seed = get_area()
                    pixels = pixels[seed[1][0][0]:seed[1][1][0],seed[0][0][0]:seed[0][1][0],seed[2][0][0]:seed[2][1][0]]
                    idx_slice = pixels.shape[0]//2
                    seed = {v:[] for v in range(len(pixels.shape))}
                    set_default(pixels, f_name)
                    np.save(save_path+f_name.replace('.npy',''),pixels)
                    done = True
                    break
                if(event.key == 115): #s
                    print(seed)

                    
            if event.type == pygame.KEYUP:
                if(event.key == 304):
                    shift = False
                    if(seed):
                        render = True
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if(event.dict['button'] == 1): #add pixel
                    v = event.dict['pos']
                    print("Semente %s"%str(v))
                    seed[show_mode].append(v)
                    if(show_mode == 0):
                        seed[2].append((v[1], idx_slice))
                        seed[1].append((idx_slice, v[0]))
                    elif(show_mode == 1):
                        seed[0].append((v[1], idx_slice))
                        seed[2].append((idx_slice, v[0]))
                    elif(show_mode == 2):
                        seed[1].append((v[1], idx_slice))
                        seed[0].append((idx_slice, v[0]))
                    if(not shift):
                        render = True

                if(event.dict['button'] == 3): #reseta
                    render_pixels = pixels.copy()
                    seed = {v:[] for v in range(len(pixels.shape))}

                if(event.dict['button'] == 4 or event.dict['button']  == 5):
                    print('Slice %d'%idx_slice)
                    render = True
                if(event.dict['button'] == 4): #+threshold
                    if(shift):
                        idx_slice = min(idx_slice + 10,pixels.shape[0]-1)
                    else:
                        idx_slice = min(idx_slice + 1,pixels.shape[0]-1)
                if(event.dict['button'] == 5): #-threshold
                    if(shift):
                        idx_slice = max(idx_slice - 10,0)
                    else:
                        idx_slice = max(idx_slice - 1,0)

        

        show_pixels(pixels[idx_slice], seed)
        pygame.display.update()
        clock.tick(60)
    # ===========================================================================
