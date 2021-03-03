import mapreader
import pygamegui as gui


gui.StartPygame()
gui.DrawMap()
mapreader.InitMapBlocks()
gui.Update()

while True:
    gui.Update()
    gui.clock.tick(gui.FPS)