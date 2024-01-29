"""
Based on this project: https://github.com/naseer2426/Three-Dimention-Rendering-Tk
Modified by Akascape
"""

import tkinter 
import math as m
import time as t

class ThreeDFrame(tkinter.Canvas):
    
    def __init__(self,
                 master,
                 coords,
                 angles: tuple = (0,0,90),
                 fps: int = 60,
                 size: int = 100,
                 **kwargs):
       
        super().__init__(master=master, highlightthickness=0, borderwidth=0, **kwargs)
        
        self.geometry = ThreeD(self, coords, alpha=angles[0], beeta=angles[1], gaama=angles[2], frame_rate=fps, unit_pixels=size)
        self.geometry.print_object()
        self.geometry.dynamic_movement()
        self.angles = angles
        self.coords = coords
        self.fps = fps
        self.size = size

    def configure(self, **kwargs):

        if "size" in kwargs:
            self.size = kwargs.pop("size")
            
        if "fps" in kwargs:
            self.fps = kwargs.pop("fps")

        if "coords" in kwargs:
            self.coords = kwargs.pop("coords")

        if "angles" in kwargs:
            self.angles = kwargs.pop("angles")
            
        super().config(**kwargs)

        self.delete("all")

        self.geometry = ThreeD(self, self.coords, alpha=self.angles[0], beeta=self.angles[1], gaama=self.angles[2],
                               frame_rate=self.fps, unit_pixels=self.size)
        self.geometry.print_object()
        self.geometry.dynamic_movement()
        
class ThreeD():

    def __init__(self,
                 canvas,
                 coords,
                 alpha = 0,
                 beeta = 0,
                 gaama = 0,
                 frame_rate = 90,
                 unit_pixels = 100):

        self.canvas = canvas
        self.coords = self.set_coords(coords)
        self.alpha = alpha
        self.beeta = beeta
        self.gaama = gaama
        self.frame_rate = frame_rate
        self.unit_pixels = unit_pixels
        self.printed_polygons = []
        self.set_view_dist()
        self.set_canvas_size()
        self.set_color()
        self.set_view_point()
        self.set_virtual_axis()
        not_error = not(self.set_surface_equations())

        
        if not_error:
            raise Exception("Coplaner Issue")
    @staticmethod
    def dist(point1, point2):
        x1,y1,z1 = point1
        x2,y2,z2 = point2

        return m.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

    @staticmethod
    def set_coords(coords):
        points = coords[0]
        final_coords = []
        for surface in coords[1:]:
            s = []
            for polygon in surface:
                p = []

                for point in polygon[:-1]:
                    p.append(points[point])

                p.append(polygon[-1])
                s.append(p)

            final_coords.append(s)

        return final_coords

    def set_view_dist(self):
        self.d = 0
        points = self.distinct_points()
        for point in points:
            distance = self.dist(point,(0,0,0))
            if distance>self.d:
                self.d = distance
        self.d*=50

    def set_view_point(self, view_point = None, reference_point = None):
        if view_point == None and reference_point == None:
            self.a = m.cos(self.beeta) * m.sin(self.alpha)
            self.b = m.sin(self.beeta)
            self.c = m.cos(self.beeta) * m.cos(self.alpha)

            reference_point = self.rotate_zaxis((0,1,0), theeta = self.gaama)
            self.set_virtual_axis(reference_point)
        else:
            self.a, self.b, self.c = view_point
            self.set_virtual_axis(reference_point)

    def distinct_points(self):
        points = []
        for surface in self.coords:
            for polygon in surface:
                for point in polygon[:-1]:
                    if point not in points:
                        points.append(point)
        return points

    def set_canvas_size(self):
        self.csize = 0
        points = self.distinct_points()
        for point in points:
            distance = self.dist(point,(0,0,0))
            if distance>self.csize:
                self.csize = distance
        self.csize = int(self.csize*2*self.unit_pixels)+50
        #self.canvas.config(width = self.csize, height = self.csize)

    @staticmethod
    def plane_equation(point1, point2, point3):
        x1,y1,z1 = point1
        x2,y2,z2 = point2
        x3,y3,z3 = point3

        a = (y2-y1)*(z3-z1)-(y3-y1)*(z2-z1)
        b = (x3-x1)*(z2-z1)-(x2-x1)*(z3-z1)
        c = (x2-x1)*(y3-y1)-(x3-x1)*(y2-y1)
        d = a*x1 + b*y1 + c*z1

        return [a,b,c,d]

    def set_surface_equations(self):
        self.s_equations = []
        for surface in self.coords:
            point1 = surface[0][0]
            point2 = surface[0][1]
            point3 = surface[0][2]

            self.s_equations.append(self.plane_equation(point1,point2,point3))
            
            for polygon in surface:
                for point in polygon[:-1]:
                    x,y,z = point
                    a,b,c,d = self.s_equations[-1]
                    if a*x + b*y + c*z != d:
                        return 0

        return 1

    def display_list(self):
        l = []

        for equation in self.s_equations:
            A,B,C,D = equation
            x,y,z = self.d*self.a,self.d*self.b,self.d*self.c
            l.append(A*x + B*y + C*z >= D)

        return l



    def display_surfaces(self,coords):
        d_list = self.display_list()
        d_surface = []

        for i in range(len(d_list)):
            if d_list[i]:
                d_surface.append(coords[i])

        return d_surface

    def threeD_to_twoD(self):
        return_coords = []
        for surface in self.coords:
            return_surface = []
            for polygon in surface:
                return_polygon = []
                for point in polygon[:-1]:
                    x,y,z = point
                    a,b,c = self.a, self.b, self.c

                    X = x*(b**2+c**2) - y*(a*b) - z*(a*c)
                    Y = y*(a**2+c**2) - z*(b*c) - x*(a*b)
                    Z = z*(a**2+b**2) - y*(b*c) - x*(a*c)

                    lamda = m.sqrt(b**2+c**2)
                    v = m.sqrt(a**2+b**2+c**2)
                    if lamda == 0:
                        lamdax = 1
                        c=1
                    else:
                        lamdax = lamda

                    X,Y,Z = self.rotate_xaxis((X,Y,Z), cos_val = c/lamdax, sin_val = b/lamdax)
                    X,Y,Z = self.rotate_yaxis((X,Y,Z), cos_val = lamda/v, sin_val = -a/v)

                    new_vxaxis = self.rotate_xaxis(self.vxaxis, cos_val = c/lamdax, sin_val = b/lamdax)
                    new_vxaxis = self.rotate_yaxis(new_vxaxis, cos_val = lamda/v, sin_val = -a/v)

                    new_referencepoint = self.rotate_xaxis(self.reference_point, cos_val = c/lamdax, sin_val = b/lamdax)
                    new_referencepoint = self.rotate_yaxis(new_referencepoint, cos_val = lamda/v, sin_val = -a/v)

                    if new_vxaxis[1]>=0 and new_referencepoint[1]>=0:
                        gaama = m.asin(new_vxaxis[1])
                    elif new_referencepoint[1]<=0:
                        gaama = m.pi - m.asin(new_vxaxis[1])
                    else:
                        gaama = 2*m.pi + m.asin(new_vxaxis[1])

                    X,Y,Z = self.rotate_zaxis((X,Y,Z),theeta = -gaama)
                    X = X*self.unit_pixels + self.csize/2
                    Y = self.csize/2 - Y*self.unit_pixels
                    return_polygon.append((X,Y))
                return_polygon.append('#%02x%02x%02x' % polygon[-1])

                return_surface.append(return_polygon)
            return_coords.append(return_surface)
       
        return return_coords

    def delete_polygon(self):
        for polygon in self.printed_polygons:
            self.canvas.delete(polygon)

        self.printed_polygons = []

    def print_object(self , during_animation = 0):
        self.delete_polygon()
        twoD_coords = self.display_surfaces(self.threeD_to_twoD())
        self.dynamic_colors()
        for surface in twoD_coords:
            for polygon in surface:
                self.printed_polygons.append(self.canvas.create_polygon(polygon[:-1], fill = polygon[-1]))
        self.canvas.update()

        if during_animation:
            t.sleep(1/self.frame_rate)

    def change_angles(self, change_alpha, change_beeta, change_gaama):
        self.alpha += change_alpha
        self.beeta += change_beeta
        self.gaama += change_gaama
        self.set_view_point()

    def set_angles(self, alpha = None, beeta = None, gaama = None):
        if alpha == None and beeta == None and gaama ==None:
            pass
        else:
            self.alpha = alpha
            self.beeta = beeta
            self.gaama = gaama
            self.set_view_point()

    @staticmethod
    def rotate_xaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        Y = y*cos_val - z*sin_val
        Z = y*sin_val + z*cos_val

        return (x,Y,Z)

    @staticmethod
    def rotate_yaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        X = x*cos_val + z*sin_val
        Z = -x*sin_val + z*cos_val

        return (X,y,Z)

    @staticmethod
    def rotate_zaxis(point, theeta = None, cos_val = None, sin_val = None):
        if cos_val == None:
            cos_val = m.cos(theeta)
        if sin_val == None:
            sin_val = m.sin(theeta)

        x,y,z = point
        X = x*cos_val - y*sin_val
        Y = x*sin_val + y*cos_val

        return (X,Y,z)

    def rotate_point_about_line(self, point, angle, line_vector):
        a,b,c = line_vector
        lamda = m.sqrt(b**2+c**2)
        v = m.sqrt(a**2+b**2+c**2)
        if lamda == 0:
            lamdax = 1
            c=1
        else:
            lamdax = lamda

        p = self.rotate_xaxis(point, cos_val = c/lamdax, sin_val = b/lamdax)
        p = self.rotate_yaxis(p, cos_val = lamda/v, sin_val = -a/v)
        p = self.rotate_zaxis(p, theeta = angle)
        p = self.rotate_yaxis(p, cos_val = lamda/v, sin_val = a/v)
        p = self.rotate_xaxis(p, cos_val = c/lamdax, sin_val = -b/lamdax)

        return p

    def set_virtual_axis(self, reference_point = (0,1,0)):
        self.reference_point = reference_point
        x1,y1,z1 = reference_point
        x2,y2,z2 = self.a,self.b,self.c
        self.vxaxis = (y1*z2-y2*z1, x2*z1-x1*z2, x1*y2-x2*y1)

    def set_first_click(self, event):
        self.mouse_loc = (event.x, event.y)

    def change_view_angle(self, event):
        self.canvas.unbind('<B1-Motion>', self.move)
        x_diff = event.x - self.mouse_loc[0]
        y_diff = event.y - self.mouse_loc[1]
        const = m.pi/(self.unit_pixels*4)
        alpha_change = -x_diff * const
        beeta_change = y_diff * const

        new_viewpoint = self.rotate_point_about_line((self.a,self.b,self.c),alpha_change,self.reference_point)
        new_viewpoint = self.rotate_point_about_line(new_viewpoint,-beeta_change,self.vxaxis)
        new_referencepoint = self.rotate_point_about_line(self.reference_point,-beeta_change,self.vxaxis)

        self.set_view_point(new_viewpoint,new_referencepoint)

        self.print_object(1)
   
        self.mouse_loc = (event.x, event.y)
        self.move = self.canvas.bind('<B1-Motion>', self.change_view_angle)

    def dynamic_movement(self):
        self.start_move = self.canvas.bind('<Button-1>', self.set_first_click)
        self.move = self.canvas.bind('<B1-Motion>', self.change_view_angle)

    def stop_dynamic_movement(self):
        self.canvas.unbind('<Button-1>', self.start_move)
        self.canvas.unbind('<B1-Motion>',self.move)

    def change_color(self, colors):
        for i in range(len(self.coords)):
            for j in range(len(self.coords[i])):
                self.colors[i][j][-1] = colors[i][j]

    def set_color(self, colors = None):
        if colors == None:
            self.colors = []
            for surface in self.coords:
                s = []
                for polygon in surface:
                    s.append(polygon[-1])
                self.colors.append(s)
        else:
            self.colors = colors

    def dynamic_colors(self):

        a1,b1,c1 = self.a,self.b,self.c

        for i in range(len(self.coords)):
            a2,b2,c2 = self.s_equations[i][0],self.s_equations[i][1],self.s_equations[i][2]
            d = self.dist((a2,b2,c2),(0,0,0))
            a2,b2,c2 = a2/d,b2/d,c2/d

            cos_angle = a1*a2+b1*b2+c1*c2
            if cos_angle>=0:
                for j in range(len(self.coords[i])):
                    r,g,b = self.colors[i][j]
                    r,g,b = r*cos_angle + r/3*(1-cos_angle),g*cos_angle + g/3*(1-cos_angle),b*cos_angle + b/3*(1-cos_angle)
                    self.coords[i][j][-1] = (int(r),int(g),int(b))
   
