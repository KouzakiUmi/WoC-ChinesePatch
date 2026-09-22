init python:
    import math
    import random

    class ParticleDef:

        def __init__(self, path, count, z_index, x_speed, y_speed, rotation_speed, leaf):
            self.path = path
            self.count = count
            self.z_index = z_index
            self.x_speed = x_speed
            self.y_speed = y_speed
            self.rotation_speed = rotation_speed
            self.leaf = leaf
            self.displayable = renpy.displayable(path)

            # Get image dimensions
            r = renpy.render(self.displayable, 2048, 2048, 0, 0)
            self.width, self.height = r.get_size()
            self.width = int(self.width)
            self.height = int(self.height)


    class ParticleDisplayable(renpy.Displayable):

        def __init__(self, part_def):
            renpy.Displayable.__init__(self)
            self.part_def = part_def
            self.displayable = part_def.displayable
            self._last_at = None
            self._genparams()
            self._setinitpos()

        def _genparams(self):
            self.x_speed = math.copysign(0.7 + abs(random.random() * self.part_def.x_speed), self.part_def.x_speed) * 60
            self.y_speed = math.copysign(0.7 + abs(random.random() * self.part_def.y_speed), self.part_def.y_speed) * 60
            self.rotation_speed = math.copysign(1.72 + abs(random.random() * self.part_def.rotation_speed / (2 * math.pi) * 360),
                                                self.part_def.rotation_speed) * 60

            self.rotate = random.randrange(360)
            self._orig_scale = 0.5 + random.random() * 0.5
            self.xzoom = self._orig_scale
            self.yzoom = self._orig_scale

            self.update_leaf = self.part_def.leaf
            if self.update_leaf:
                self.leaf_delay = (120 + random.randrange(180)) / 60.0

            self.alpha = 0.0

        def _setinitpos(self):
            # Initial position
            self.xpos = random.randrange(-self.part_def.width, config.screen_width + 2 * self.part_def.width)
            self.ypos = random.randrange(-self.part_def.height, config.screen_width + 2 * self.part_def.height)

        def _setnewpos(self):
            # Assume only going to the right and down
            self.xpos = random.randrange(-config.screen_width // 2, config.screen_width)
            self.ypos = -self.part_def.height * 3

        def reset(self):
            self._genparams()
            self._setnewpos()

        def _needreset(self):
            # Assume only going to the right and down
            return self.xpos > config.screen_width + self.part_def.width * 3 \
                or self.ypos > config.screen_height + self.part_def.height * 3

        def render(self, width, height, st, at):
            if self._last_at is None or at < self._last_at:
                self._last_at = at

            dt = at - self._last_at
            self._last_at = at

            self.xpos += self.x_speed * dt
            self.ypos += self.y_speed * dt
            self.rotate += self.rotation_speed * dt
            if self.alpha < 1:
                new_alpha = self.alpha + 3.52941176 * dt
                if new_alpha > 1:
                    new_alpha = 1.0
                self.alpha = new_alpha
            if self.update_leaf:
                self.leaf_delay -= dt
                if self.leaf_delay <= 0:
                    self.xzoom -= 0.6 * dt
                    if self.xzoom < -self._orig_scale:
                        self.xzoom = -self._orig_scale
                        self.update_leaf = False

            if self._needreset():
                self.reset()

            t = Transform(self.displayable, xzoom=self.xzoom, yzoom=self.yzoom,
                          rotate=self.rotate, alpha=self.alpha)

            child_render = renpy.render(t, width, height, st, at)
            w, h = child_render.get_size()
            w = int(w)
            h = int(h)
            render = renpy.Render(w, h)
            render.blit(child_render, (0,0))
            return render

        def visit(self):
            return [self.displayable]


    class TitleParticlesDisplayable(renpy.Displayable):
        def __init__(self, particles):
            renpy.Displayable.__init__(self)
            self._particles = particles

            self._live_particles = {}
            for part_def in particles:
                allocated = []
                for i in range(part_def.count):
                    allocated.append(ParticleDisplayable(part_def))
                self._live_particles[part_def] = allocated

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)

            for part_def, allocated in sorted(self._live_particles.items(), key=lambda kv: kv[0].z_index):
                for particle in allocated:
                    child_render = renpy.render(particle, width, height, st, at)
                    render.blit(child_render, (particle.xpos, particle.ypos))
                    renpy.redraw(particle, 0)

            return render

        def visit(self):
            arr = []
            for allocated in self._live_particles.values():
                arr += allocated
            return arr
