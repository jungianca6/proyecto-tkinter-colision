import tkinter as tk
import random
import time
from PIL import ImageTk,Image
import pygame
from threading import Thread

balas=[]
last_shot_time = 0.0
enemigoslista=[]
#.after
#eventos teclas tkinter
#moveq
#focus para detectar el teclado
#winfo_rootx/y()

"""def todo()
        movimiento
        ventanauqeesta.after(10,todo)

todo()"""

#nave_x
#nave_y
#nave_velocidad Nuevos vlores al presionar la tecla
def destruye_ventana(vD,vG):     #entrar y salir               
        """  
        Funcionalidad: Destruye la ventana actual
        Entradas:N/A
        Salidas:N/A
        """
        vG.deiconify()
        vD.destroy()
        
def ventana():
    ventanamain = tk.Tk()
    ventanamain.title("Space Shooters")
    ventanamain.minsize(600, 300)
    ventanamain.maxsize(600, 300)

    ventanamain.configure(background="light blue")
    ancho = 600
    largo = 400

    def about():
        aboutgame= tk.Toplevel() #se genera la pantalla que se muestra para el about
        aboutgame.title("About Game")
        aboutgame.minsize(600, 150)
        aboutgame.maxsize(600,150)
        aboutgame.configure(background="light blue")
        
    
        ventanamain.withdraw()
        
        aboutgame.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(aboutgame,ventanamain))
        
        volver = tk.Button(aboutgame, text="Volver", width=10, command=lambda:destruye_ventana(aboutgame,ventanamain))
        volver.place(x=350, y=70)

        
                

    def gamestart():
        game= tk.Toplevel() #se genera la pantalla que se muestra para el about
        game.title("Space Shooters")
        game.minsize(1000, 600)
        game.maxsize(1000,600)
        game.configure(background="#1C1A59")

        canvas= tk.Canvas(game, width= 900, height= 500,bg="black")
        canvas.pack()

        """img=ImageTk.PhotoImage(Image.open("spaceship.gif"))
        canvas.pack()
        canvas.create_image(70, 50,image=img)"""

        #Imagen de fondo
        bgspace=(Image.open('space background.gif'))
        resizedbgspace= bgspace.resize((920,518), Image.LANCZOS)
        newspace= ImageTk.PhotoImage(resizedbgspace)

        bgspace=canvas.create_image(450,250,anchor=tk.CENTER, image=newspace)
        
        #Imagen de la nave
        ship= (Image.open("spaceship.gif"))

        resizedship= ship.resize((82,75), Image.LANCZOS)
        newship= ImageTk.PhotoImage(resizedship)

        ship=canvas.create_image(10,10, anchor=tk.NW, image=newship)

        #Imagen de la bala 
        bullet= (Image.open("bullet.gif"))

        resizedbullet= bullet.resize((100,52), Image.LANCZOS)
        newbullet= ImageTk.PhotoImage(resizedbullet)

        #Imagen de alien
        alien= (Image.open("alien.gif"))

        resizedalien= alien.resize((85,57), Image.LANCZOS)
        newalien= ImageTk.PhotoImage(resizedalien)

        #Prueba alien
        def alien(canvas,newalien):
                global enemigoslista
                alien=canvas.create_image(500,350, image=newalien)
                enemigoslista.append(alien)
        alien(canvas,newalien)
        

        #Funciones de movimiento

        #Limite de movimiento
        def bordepantalla():
                borde=canvas.bbox(ship)
                x1,y1,x2,y2=borde
                if y1<10 and y2<115:
                        canvas.move(ship,0,10)  #borde arriba
                elif y1>420:
                        canvas.move(ship,0,-10) #borde abajo
                elif x1<10:
                        canvas.move(ship,10,0)  #borde izquierda
                elif x2>905:
                        canvas.move(ship,-10,0) #borde derecha

        #Movimiento
        def up(event):
                global uploop, downloop
                try:
                        game.after_cancel(uploop)
                        canvas.move(ship,0,-10)
                        uploop=game.after(10,lambda: up(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,0,-10)
                        uploop=game.after(10,lambda: up(event))
                        bordepantalla()

        def stopup(event):
                global uploop
                game.after_cancel(uploop)
         
        def down(event):
                global uploop, downloop
                try:
                        game.after_cancel(downloop)
                        canvas.move(ship,0,10)
                        downloop=game.after(10,lambda: down(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,0,10)
                        downloop=game.after(10,lambda: down(event))
                        bordepantalla()

        def stopdown(event):
                global downloop
                game.after_cancel(downloop)
                
        def left(event):
                global rightloop, leftloop
                try:
                        game.after_cancel(leftloop)
                        canvas.move(ship,-10,0)
                        leftloop=game.after(10,lambda: left(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,-10,0)
                        leftloop=game.after(10,lambda: left(event))
                        bordepantalla()

        def stopleft(event):
                global leftloop
                game.after_cancel(leftloop)
                        
        def right(event):
                global rightloop, leftloop
                try:
                        game.after_cancel(rightloop)
                        canvas.move(ship,10,0)
                        rightloop=game.after(10,lambda: right(event))
                        bordepantalla()
                except NameError:
                        canvas.move(ship,10,0)
                        rightloop=game.after(10,lambda: right(event))
                        bordepantalla()

        def stopright(event):
                global rightloop
                game.after_cancel(rightloop)
                

        #Funcion de disparo de la bala 

        
        def movelaser(id, laser, laserloop,alien):
                global balas, enemigoslista
                try:
                        bordelaser = canvas.bbox(laser)
                        x1, y1, x2, y2 = bordelaser
                        if x1 > 905:
                                canvas.delete(laser)
                                if laserloop:
                                        game.after_cancel(laserloop)
                                remove_bala(id)      
                        else:
                                canvas.move(laser, 10, 0)
                                laserloop = game.after(10, movelaser, id, laser, laserloop,alien)
                                if len(enemigoslista)>0:
                                        colisionbala(laser)

                except:
                        return

        def colisionbala(laser):
                global enemigoslista
                bordelaser = canvas.bbox(laser)
                x1, y1, x2, y2 = bordelaser
                bordealien = canvas.bbox(enemigoslista[0])
                xa1,ya1,xa2,ya2= bordealien
                if x2 > xa1 and y2 > ya1 and x1 < xa2 and y1 < ya2:
                        canvas.delete(laser)
                        canvas.delete(enemigoslista[0])
                        remove_bala(id)
                        enemigoslista.pop(0)
            

        def remove_bala(id):
                global balas
                if balas[0]['id'] == id:
                        canvas.delete(balas[0]['laser'])
                        game.after_cancel(balas[0]['laserloop'])
                        balas.pop(0)
                elif len(balas) > 1:
                        balas = balas[1:]
                        remove_bala(id)

        def shoot(event): #crea bala
                global balas, last_shot_time

                current_time= time.monotonic()
                if current_time - last_shot_time>=0.5:  #cooldown
                        last_shot_time = current_time
                        try:
                                game.after_cancel(balas[0]['laserloop'])
                                bordenave = canvas.bbox(ship)
                                x1, y1, x2, y2 = bordenave
                                #posicion de bala
                                xbala = x2 + 15
                                ybala = (y1 + y2) / 2
                                laser = canvas.create_image(xbala, ybala, image=newbullet)
                                id = canvas.create_text(xbala, ybala, text='', fill='white', font=('arial', 1))
                                laserloop = game.after(10, movelaser, id, laser, None,alien)
                                balas.append({'id': id, 'laser': laser, 'laserloop': laserloop})
                                
                                pygame.mixer.init()
                                blastsound=pygame.mixer.Sound('blast shot.wav')
                                blastsound.play()
                                blastsound.set_volume(0.3)
                        
                        except IndexError:
                                bordenave = canvas.bbox(ship)
                                x1, y1, x2, y2 = bordenave
                                xbala = x2 + 20
                                ybala = (y1 + y2) / 2
                                laser = canvas.create_image(xbala, ybala, image=newbullet)
                                id = canvas.create_text(xbala, ybala, text='', fill='white', font=('arial', 1))
                                laserloop = game.after(5, movelaser, id, laser, None,alien)
                                balas.append({'id': id, 'laser': laser, 'laserloop': laserloop})

                                pygame.mixer.init()
                                blastsound=pygame.mixer.Sound('blast shot.wav')
                                blastsound.play()
                                blastsound.set_volume(0.3)
                                
      
        #Funciones de Tecla
                
        game.bind("<Up>",up)
        game.bind("<Down>",down)
        game.bind_all("<Left>",left)
        game.bind_all("<Right>",right)
        game.bind_all("<space>",shoot)

        game.bind_all("<KeyRelease - Left>",stopleft)
        game.bind_all("<KeyRelease - Right>",stopright)
        game.bind_all("<KeyRelease - Up>",stopup)
        game.bind_all("<KeyRelease - Down>",stopdown)

   
        ventanamain.withdraw()
        
        game.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(game,ventanamain))

        #Boton de Regreso
        volver = tk.Button(game, text="Volver", width=10, command=lambda:destruye_ventana(game,ventanamain))
        volver.place(x=900, y=570)
        

        ventanamain.mainloop()

    def highscore():
        hiscore= tk.Toplevel() #se genera la pantalla que se muestra para el about
        hiscore.title("High Scores")
        hiscore.minsize(600, 150)
        hiscore.maxsize(600,150)
        hiscore.configure(background="light blue")

        ventanamain.withdraw()
        
        hiscore.protocol('WM_DELETE_WINDOW', lambda:destruye_ventana(hiscore,ventanamain))
        
        volver = tk.Button(hiscore, text="Volver", width=10, command=lambda:destruye_ventana(hiscore,ventanamain))
        volver.place(x=350, y=70)



    aboutthegame = tk.Button(ventanamain,text= "About the game" ,padx=10,pady=10,command=about)
    aboutthegame.place(x=210,y=20)
#---------------------------------------------------------------------------------------------------------------------
    gamebegin = tk.Button(ventanamain,text= "Start game",padx=10,pady=10,command=gamestart)
    gamebegin.place(x=210,y=80)
#---------------------------------------------------------------------------------------------------------------------
    HIscore = tk.Button(ventanamain,text= "High Score" ,padx=10,pady=10,command=highscore)
    HIscore.place(x=210,y=140)
    ventanamain.mainloop()
ventana()

"""def game_loop():
    # Actualizar estado del juego
    update_game_state()

    # Redibujar pantalla
    redraw_screen()

    # Verificar si el juego ha terminado
    if not game_over():
        # Esperar un tiempo antes de llamar a la función de nuevo
        root.after(10, game_loop)"""
"""def play():
        pygame.mixer.init()
        pygame.mixer.music.load("On Melancholy Hill.wav")
        pygame.mixer.music.play(0)

    canvasC1 = tk.Canvas(ventanamain, width=300, height=200, borderwidth=0, highlightthickness=0, bg="black")
    canvasC1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    img=ImageTk.PhotoImage(Image.open("gorillaz.gif"))
    canvasC1.pack()

    canvasC1.create_image(100, 50, image=img)

    play=tk.Button(ventanamain, text="Play song", width=10,command=play)
    play.place(x=350, y=250)
"""
"""def move(img, dx, dy):
                canvas.move(img, dx, dy)
                x, y, w, h = canvas.coords(img)
                if x < 0:
                        move(img, -x, 0)
                elif x + w > canvas.winfo_width():
                        move(img, canvas.winfo_width() - (x + w), 0)
                if y < 0:
                        move(img, 0, -y)
                elif y + h > canvas.winfo_height():
                        move(img, 0, canvas.winfo_height() - (y + h))"""

"""borde4=canvas.bbox(ship)
                x1,y1,x2,y2=borde4
                print(borde4)"""
