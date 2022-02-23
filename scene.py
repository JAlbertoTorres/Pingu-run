class Scene:

	def __init__(self, director):
			self.director = director

	def on_update(self):
		"Actualización lógica que se llama automáticamente desde el director"
		raise NoImplemented("Tiene que implementar el método on_update.")

	def on_event(self, event):
		"Se llama cuando llega un evento especifico al bucle"
		raise NoImplemented("Tiene que implementar el método on_event.")

	def on_draw(self, screen):
		"Se llama cuando se quiere dibujar la pantalla"
		raise NoImplemented("Tiene que implementar el método on_draw.")