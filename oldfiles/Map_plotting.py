import matplotlib.pyplot as plt
import rasterio
import numpy as np
from cartopy import crs
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from shapely.geometry import Point


class MapPlotting:

    def __init__(self, bg_path, path, user_input, highest_point, nearest_node, highest_node, clipped_path):
        self.bg_path = bg_path
        self.path = path
        self.user_input = user_input
        self.highest_point = highest_point
        self.nearest_node = nearest_node
        self.highest_node = highest_node
        self.clipped_ele = rasterio.open(clipped_path)
        self.background = rasterio.open(self.bg_path)
        self.back_array = self.background.read(1)

    def plot_map(self, buffer_area):
        """
        Draw the shortest route from the nearest node to the highest node in the buffer, the base map, your position,
        your target position, legend, scale, elevation, etc.
        :return:
        """
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        # plot buffer and background
        buffer = plt.Circle((self.user_input.x, self.user_input.y), buffer_area, color="purple", alpha=0.2, zorder=2)
        ax.add_patch(buffer)
        palette = np.array([value for key, value in self.background.colormap(1).items()])
        background_image = palette[self.back_array]
        bounds = self.background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [self.user_input.x-buffer_area, self.user_input.x+buffer_area, self.user_input.y-buffer_area,
                          self.user_input.y+buffer_area]
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        ax.set_extent(display_extent, crs=crs.OSGB())

        # plot path
        self.path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=3)

        # plot points
        your_location, = plt.plot(self.user_input.x, self.user_input.y, 'o', color='blue', markersize=0.6, zorder=4)
        highest_p, = plt.plot(self.highest_point.x, self.highest_point.y, '^', color='blue', markersize=2, zorder=4)
        nearest_n, = plt.plot(self.nearest_node.x, self.nearest_node.y, 'o', color='red', markersize=0.6, zorder=5)
        highest_n, = plt.plot(self.highest_node.x, self.highest_node.y, '^', color='red', markersize=2, zorder=5)

        # plot elevation and colorbar
        clipped_array = self.clipped_ele.read(1)
        clipped_array[clipped_array == 0] = np.NAN
        ele_bounds = self.clipped_ele.bounds
        ele_extent = [ele_bounds.left, ele_bounds.right, ele_bounds.bottom, ele_bounds.top]
        ele_show = ax.imshow(clipped_array,
                                  interpolation='nearest', extent=ele_extent, origin="upper",
                                  cmap='terrain', zorder=3, alpha=0.3)
        elebar = plt.colorbar(ele_show, fraction=0.07, pad=0.1)
        elebar.ax.tick_params(labelsize=4)

        # plot the scale bar,
        fontprops = fm.FontProperties(size=4)
        scalebar = AnchoredSizeBar(ax.transData,
                                   2000, '2 km', loc=4,
                                   pad=0.7, color='black', frameon=False,
                                   size_vertical=8, fontproperties=fontprops,)
        ax.add_artist(scalebar)

        # plot the north arrow
        loc_x = 0.9
        loc_y = 0.88
        width = 0.02
        height = 0.05
        pad = 0
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
        ylen = maxy - miny
        xlen = maxx - minx
        left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
        right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
        top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
        center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
        triangle = mpatches.Polygon([left, top, right, center], color='k')
        ax.text(
            s='N',
            x=minx + xlen * loc_x, y=miny + ylen * (loc_y - pad + height) * 1.02,
            fontsize=6, horizontalalignment='center', verticalalignment='bottom')
        ax.add_patch(triangle)

        # plot the legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        buffer_l = mpatches.Patch(color="purple", alpha=0.1, label="5km Area")
        shortest_line = mlines.Line2D([], [], linewidth=1, color="blue", markersize=8, label="Shortest Path")
        plt.legend([buffer_l, shortest_line, your_location, highest_p, nearest_n, highest_n],
                   ["Buffer area", "The shortest path", "Your location", "The highest point", "The nearest node",
                    "The highest node"],
                   loc="upper left", fontsize=4)

        # plot title
        plt.title("Emergency Path Planning (for walk)", fontsize=8)
        plt.show()

        return

    def plot_drive_path(self, path):
        """
        Draw a route to the highest point on the island using transportation
        :param path:
        :return:
        """
        highest_point_island = Point(456967.5, 78547.5)
        highest_node = Point(456960.316, 78564.546)
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())

        # plot background
        palette = np.array([value for key, value in self.background.colormap(1).items()])
        background_image = palette[self.back_array]
        bounds = self.background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        ax.set_extent(extent, crs=crs.OSGB())

        # plot path
        path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=3)

        # plot points
        your_location, = plt.plot(self.user_input.x, self.user_input.y, 'o', color='blue', markersize=0.6, zorder=4)
        highest_p, = plt.plot(highest_point_island.x, highest_point_island.y, '^', color='blue', markersize=2, zorder=4)
        nearest_n, = plt.plot(self.nearest_node.x, self.nearest_node.y, 'o', color='red', markersize=0.6, zorder=5)
        highest_n, = plt.plot(highest_node.x, highest_node.y, '^', color='red', markersize=2, zorder=5)

        # plot the scale bar,
        fontprops = fm.FontProperties(size=4)
        scalebar = AnchoredSizeBar(ax.transData,
                                   5000, '20 km',
                                   loc=4, pad=0.7, color='black', frameon=False,
                                   size_vertical=8, fontproperties=fontprops, )
        ax.add_artist(scalebar)

        # plot the north arrow
        loc_x = 0.9
        loc_y = 0.87
        width = 0.02
        height = 0.05
        pad = 0
        minx, maxx = ax.get_xlim()
        miny, maxy = ax.get_ylim()
        ylen = maxy - miny
        xlen = maxx - minx
        left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
        right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
        top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
        center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
        triangle = mpatches.Polygon([left, top, right, center], color='k')
        ax.text(
            s='N',
            x=minx + xlen * loc_x, y=miny + ylen * (loc_y - pad + height) * 1.02,
            fontsize=6, horizontalalignment='center', verticalalignment='bottom')
        ax.add_patch(triangle)

        # plot the legend
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)
        shortest_line = mlines.Line2D([], [], linewidth=1, color="blue", markersize=8, label="Shortest Path")
        plt.legend([shortest_line, your_location, highest_p, nearest_n, highest_n],
                   ["The shortest path", "Your location", "The highest point", "The nearest node", "The highest node"],
                   loc="upper left", fontsize=3)

        # plot title
        plt.title("Emergency Path Planning (by vehicle)", fontsize=8)

        plt.show(block=False)

        return
