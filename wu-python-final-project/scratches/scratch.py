# Scrapping this for now.
# GPolygon doesn't work well, plus getting the object to move like I want is taking up too much time, and it's not different
# enough from the movements of the bouncing ball anyway.
class ZippingTarget(GameObject):
    def __init__(self, parent_window: GWindow):
        GameObject.__init__(self, parent_window)
        self._dest_x = 0
        self._dest_y = 0

        # GPolygon objects are broken. Positioning them with set_location() doesn't work right. Even watching variables
        # change in a debugger you can see that the x,y coordinates within the GPolygon are correct, but the object
        # doesn't display on screen right and blasts off in seemingly random directions off of the window.
        # self.visible_shape(make_triangle(60))
        self.visible_shape(make_centered_circle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 40, "orange", "blue", 5))

        set_object_color(self.visible_shape(), "blue", "black", 3)
        self._dx = self._dest_x - self.x()
        self._dy = self._dest_y - self.y()

        # self.visible_shape().set_location(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        center_object_at(self.visible_shape(), self.x(), self.y())

    def _at_destination(self, variance: int = 0) -> bool:
        return (self._dest_x - variance <= self.x() <= self._dest_x + variance) and (
                self._dest_y - variance <= self.y() <= self._dest_y + variance)

    def update(self):
        if self._at_destination(variance=1):
            self._dest_x = random.randint(0, WINDOW_WIDTH)
            self._dest_y = random.randint(0, WINDOW_HEIGHT)
            self._dx = self._dest_x - self.x()
            self._dy = self._dest_y - self.y()

        # Move toward the destination.
        # self.x(self.x() + self._dx * 0.001)
        # self.y(self.y() + self._dy * 0.001)
        self.x(self.x() + 5*(self._dx / (self._dx + self._dy)))
        self.y(self.y() + 5*(self._dy / (self._dx + self._dy)))

        # self.visible_shape().set_location(self.x(), self.y())
        center_object_at(self.visible_shape(), self.x(), self.y())