try:
	import imageio
	_imageio_imported = True
except ImportError:
	print("Please install imageio (2.1.2) for advance visualisation")
	_imageio_imported = False
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors


class MSEPlot:
	def __init__(self):
		self.xdata = []
		self.ydata = []
		self.err_type = []

	# err_type: 0 means training MSE, 1 means testing MSE
	def add_point(self, epoch, error, err_type):
		self.xdata.append(epoch)
		self.ydata.append(error)
		self.err_type.append(err_type)

	def show(self):
		color_name = ["Training MSE", "Validation MSE"]
		formatter = plt.FuncFormatter(lambda i, *args: color_name[int(i)])
		fig1 = plt.figure(1)
		plt.scatter(self.xdata, self.ydata, c = self.err_type, cmap = plt.cm.get_cmap("RdBu", 2), s = 2)
		plt.xlabel("Iteration")
		plt.ylabel("Error")
		plt.colorbar(ticks = [0, 1], format = formatter)
		plt.gca().set_ylim([0, 0.4])
		plt.show()
		plt.clf()

class ArraysPlot:
	def __init__(self, file_prefix, weight_name):
		self.images = []
		self.weight_name = weight_name
		self.file_prefix = str(file_prefix)

	def add_instance(self, array, epoch):
		file_name = "./visualize/"+self.file_prefix+"-"+str(len(self.images)).zfill(5)+".png"
		self.images.append(file_name)
		fig2 = plt.figure(2)
		cmap = colors.LinearSegmentedColormap.from_list('my_colormap', ['blue','black','red'], 256)
		img = plt.imshow(array, interpolation='nearest', cmap = cmap, origin='lower')
		plt.title("Visualization of Weight ("+self.weight_name+") (Iteration = "+str(epoch)+")")
		plt.ylabel("Nodes of Current Layer")
		plt.xlabel("Nodes of Next Layer")
		plt.colorbar(img,cmap=cmap)
		fig2.savefig(file_name)
		plt.clf()

	def generate_animation(self, output_suffix):
		if not _imageio_imported:
			return
		with imageio.get_writer('./visualize/'+self.file_prefix+"-"+output_suffix+".gif", mode='I', duration = 0.15) as writer:
			for image_path in self.images:
				image = imageio.imread(image_path)
				writer.append_data(image)

	def delete_instances(self):
		for image_path in self.images:
			os.remove(image_path)
		self.images = []