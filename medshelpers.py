import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pylab

def ddz(var, z):
	# compute the derivative of var wrt to z.

	slope = []

	for i in range(len(var)-1):
		slope.append((var[i+1] - var[i]) / (z[i+1] - z[i]))

	return slope

def clean(t, z):
	# strip 99.99 values from temperature list, and corresponding depths

	z_clean = [level for i, level in enumerate(z) if t[i] != 99.99 ]
	t_clean = [level for level in t if level != 99.99]

	return t_clean, z_clean

def is_subset(qc, result):

	combined = [a or b for a, b in zip(qc, result)]

	return sum(qc) == sum(combined)

def process_result(QC, p, result, test, filename, index, wire_break):

	if True in result:
		if not is_subset(QC, result): 
			print test + ' false positive', filename, index
			plot_profile(QC, filename, index, p)
			return 0
		elif not wire_break:
			return 1
	return 0

def plot_profile(QC, filename, index, p):
    flags = [int(x) for x in QC]
    title = filename[5:] + '-' + str(index)
    fig = plt.scatter(p.z(),p.t(),c=flags,marker='o',lw=0)
    plt.xlabel('Depth [m]')
    plt.ylabel('Temperature [C]')
    plt.title(title)
    pylab.ylim([-10,40])
    pylab.xlim([0,min([4000, p.z()[-1]])])
    plt.text(20,38, 'Lat: ' + str(p.latitude()))
    plt.text(20,36, 'Long: ' + str(p.longitude()))
    plt.text(20,34, 'Date: ' + str(p.year()) + '/' + str(p.month()) + '/' + str(p.day())    )
    plt.show()