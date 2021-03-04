import mapreader, overlord
import pygamegui as gui


gui.StartPygame()
gui.DrawMap()
mapreader.InitMapBlocks()
gui.Update()

overlord.overlord.SpawnAgents()
overlord.overlord.GetWood()
while True:
    overlord.overlord.UpdateAgents()
    gui.Update()
    gui.clock.tick(gui.FPS)