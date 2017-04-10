import entity
import constant

entities = []
for i in range(10):
	entities.append(entity.Spike([200+entity.Spike.width*i, constant.HEIGHT-entity.Spike.height]))
	
entities.append(entity.Wall([200, 200], 100, 100))
entities.append(entity.Box([250, 150], 40))
#~ entities.append(entity.Exit([constant.WIDTH-entity.Exit.width - 20, constant.HEIGHT-entity.Exit.height - 20]))

def draw(windowSurface):
	for i in entities:
		i.draw(windowSurface)
		
def update(player):
	for i in entities:
		i.update(player)