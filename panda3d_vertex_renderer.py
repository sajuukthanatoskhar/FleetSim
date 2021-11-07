from panda3d.core import *
from direct.showbase.ShowBase import ShowBase


VERT_SHADER = """
    #version 420

    uniform mat4 p3d_ModelViewProjectionMatrix;
    in vec4 p3d_Vertex;
    in int index;
//    uniform int index_offset;
    flat out int oindex;

    void main() {
        gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;
        oindex = index;// + index_offset;
    }
"""

FRAG_SHADER = """
    #version 420

    layout(r32i) uniform iimageBuffer selections;
    flat in int oindex;

    void main() {
        // Write 1 to the location corresponding to the custom index
        imageAtomicOr(selections, (oindex >> 5), 1 << (oindex & 31));
    }
"""


def create_points():

    # Define GeomVertexArrayFormats for the various vertex attributes.

    array = GeomVertexArrayFormat()
    array.add_column(InternalName.make("vertex"), 3, Geom.NT_float32, Geom.C_point)
    array.add_column(InternalName.make("color"), 4, Geom.NT_uint8, Geom.C_color)
    array.add_column(InternalName.make("index"), 1, Geom.NT_int32, Geom.C_index)

    vertex_format = GeomVertexFormat()
    vertex_format.add_array(array)
    vertex_format = GeomVertexFormat.register_format(vertex_format)

    vertex_data = GeomVertexData("point_data", vertex_format, Geom.UH_static)
    vertex_data.set_num_rows(8)

    pos_writer = GeomVertexWriter(vertex_data, "vertex")
    index_writer = GeomVertexWriter(vertex_data, "index")

    index = 0

    # create 8 points as if they were the corner vertices of a cube
    for z in (-1., 1.):
        for x, y in ((-1., -1.), (-1., 1.), (1., 1.), (1., -1.)):
            pos_writer.add_data3(x, y, z)
            index_writer.add_data1i(index)
            index += 1

    prim = GeomPoints(Geom.UH_static)
    prim.add_next_vertices(8)
    geom = Geom(vertex_data)
    geom.add_primitive(prim)
    node = GeomNode("points_geom_node")
    node.add_geom(geom)

    return node


def create_rectangle():

    vertex_format = GeomVertexFormat.get_v3()
    vertex_data = GeomVertexData("rectangle_data", vertex_format, Geom.UH_static)
    vertex_data.set_num_rows(4)

    prim = GeomLines(Geom.UH_static)
    prim.add_vertices(0, 1)
    prim.add_vertices(1, 2)
    prim.add_vertices(2, 3)
    prim.add_vertices(3, 0)
    geom = Geom(vertex_data)
    geom.add_primitive(prim)
    node = GeomNode("rectangle_geom_node")
    node.add_geom(geom)

    return node


class MyApp(ShowBase):

    def __init__(self):

        ShowBase.__init__(self)

        self.disable_mouse()
        self.camera.set_pos(0., -5., 2.)
        self.camera.look_at(0., 0., 0.)

        self._point_root = root = self.render.attach_new_node("point_root")
        point_cloud = root.attach_new_node(create_points())
        point_cloud.set_render_mode_thickness(10)

        cam = Camera("region_selection_cam")
        cam.active = False
        cam.scene = root
        self._region_sel_cam = self.camera.attach_new_node(cam)
        self._selection_cam_mask = BitMask32.bit(10)
        self._selection_color = (1., 0., 0., 1.)
        self._selection_rectangle = self.render2d.attach_new_node(create_rectangle())
        self._selection_rectangle.set_color((1., 1., 0., 1.))
        self._selection_rectangle.hide()
        self._mouse_start_pos = (0., 0.)
        self._mouse_end_pos = (0., 0.)

        self.accept("mouse1", self.__start_region_draw)
        self.accept("mouse1-up", self.__end_region_draw)

    def __start_region_draw(self):

        if not self.mouseWatcherNode.has_mouse():
            return

        screen_pos = self.mouseWatcherNode.get_mouse()
        self._mouse_start_pos = (screen_pos.x, screen_pos.y)
        self._selection_rectangle.show()
        self.task_mgr.add(self.__draw_region, "draw_region")

    def __draw_region(self, task):

        if not self.mouseWatcherNode.has_mouse():
            return task.cont

        screen_pos = self.mouseWatcherNode.get_mouse()
        x1, z1 = self._mouse_start_pos
        x2, z2 = self._mouse_end_pos = (screen_pos.x, screen_pos.y)
        geom = self._selection_rectangle.node().modify_geom(0)
        vertex_data = geom.modify_vertex_data()
        pos_writer = GeomVertexWriter(vertex_data, "vertex")
        pos_writer.set_row(0)
        pos_writer.set_data3(x1, 0., z1)
        pos_writer.set_row(1)
        pos_writer.set_data3(x1, 0., z2)
        pos_writer.set_row(2)
        pos_writer.set_data3(x2, 0., z2)
        pos_writer.set_row(3)
        pos_writer.set_data3(x2, 0., z1)

        return task.cont

    def __end_region_draw(self):

        self._selection_rectangle.hide()
        x1, y1 = self._mouse_start_pos
        x2, y2 = self._mouse_end_pos
        x1 = max(0., min(1., .5 + x1 * .5))
        y1 = max(0., min(1., .5 + y1 * .5))
        x2 = max(0., min(1., .5 + x2 * .5))
        y2 = max(0., min(1., .5 + y2 * .5))
        l, r = min(x1, x2), max(x1, x2)
        b, t = min(y1, y2), max(y1, y2)
        self.__region_select((l, r, b, t))

    def __show_selected_points(self, point_indices):

        point_cloud = self._point_root.get_child(0)
        geom = point_cloud.node().modify_geom(0)
        vertex_data = geom.modify_vertex_data()

        # first clear the point selection by making all vertices white
        new_vertex_data = GeomVertexData(vertex_data.set_color((1., 1., 1., 1.)))
        color_writer = GeomVertexWriter(new_vertex_data, "color")

        # then change the vertex color of the selected points to the selection color
        for index in point_indices:
            color_writer.set_row(index)
            color_writer.set_data4(self._selection_color)

        geom.set_vertex_data(new_vertex_data)

    def __region_select(self, frame):

        lens = self.camLens
        w, h = lens.film_size
        l, r, b, t = frame
        # compute film size and offset
        w_f = (r - l) * w
        h_f = (t - b) * h
        x_f = ((r + l) * .5 - .5) * w
        y_f = ((t + b) * .5 - .5) * h
        win_props = self.win.properties
        w, h = win_props.size  # window resolution in pixels
        # compute buffer size
        w_b = int(round((r - l) * w))
        h_b = int(round((t - b) * h))
        bfr_size = (w_b, h_b)

        if min(bfr_size) < 2:
            self.__show_selected_points([])
            return

        def get_off_axis_lens(film_size):

            lens = self.camLens
            focal_len = lens.focal_length
            lens = lens.make_copy()
            lens.film_size = film_size
            lens.film_offset = (x_f, y_f)
            lens.focal_length = focal_len

            return lens

        lens = get_off_axis_lens((w_f, h_f))
        cam_np = self._region_sel_cam
        cam = cam_np.node()
        cam.set_lens(lens)
        cam.camera_mask = self._selection_cam_mask
        tex_buffer = self.win.make_texture_buffer("tex_buffer", w_b, h_b)
        cam.active = True
        self.make_camera(tex_buffer, useCamera=cam_np)

        root = self._point_root
        point_count = 8

        tex = Texture()
        tex.setup_1d_texture(point_count, Texture.T_int, Texture.F_r32i)
        tex.clear_color = (0., 0., 0., 0.)
        shader = Shader.make(Shader.SL_GLSL, VERT_SHADER, FRAG_SHADER)

        state_np = NodePath("state_np")
        state_np.set_shader(shader, 1)
        state_np.set_shader_input("selections", tex, read=False, write=True)
        state = state_np.get_state()
        self._region_sel_cam.node().initial_state = state

        self.graphics_engine.render_frame()
        gsg = self.win.get_gsg()

        if self.graphics_engine.extract_texture_data(tex, gsg):

            texels = memoryview(tex.get_ram_image()).cast("I")
            visible_point_indices = []

            for i, mask in enumerate(texels):
                for j in range(32):
                    if mask & (1 << j):
                        index = 32 * i + j
                        visible_point_indices.append(index)

            #            print("\nVisible points:", visible_point_indices)
            self.__show_selected_points(visible_point_indices)

        else:

            #            print("\nNo points are in view.")
            self.__show_selected_points([])

        state_np.clear_attrib(ShaderAttrib)
        self.graphics_engine.remove_window(tex_buffer)
        cam.active = False


app = MyApp()
app.run()