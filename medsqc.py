import math

def end_strict_constant(p):
	# look for >50% of points in the last 50m being exactly constant
	t = p.t()
	z = p.z()
	span = 50
	i = 1
	levels = 0
	vals = {}
	qc = [False]*len(t)

	while z[-1] - z[-1*i] < span and i < len(t):
		if t[-1*i] in vals:
			vals[t[-1*i]] += 1
		else:
			vals[t[-1*i]] = 1
		levels += 1
		i += 1

	for val in vals:
		if vals[val] > levels/2.:
			qc[-1] = True

	return qc

def end_loose_constant(p):
	# look for a critical fraction of points in the last span meters falling within a tight band
	t = p.t()
	z = p.z()
	span = 100
	band = 0.1
	critical = 0.9
	temps = []
	qc = [False]*len(t)

    # get last span worth of points
    # don't tolerate any nan
	i=1
	while z[-1] - z[-1*i] < span and i < len(t):
		if(math.isnan(t[-1*i])):
			return qc
		temps.append(t[-1*i])
		i+=1

	length = len(temps)

	# only counts if this is sufficiently deep
	if z[-1*i] < 500:
		return qc

    # eliminate furthest outliers until only a cluster within band remains
	temps.sort()
	while temps[-1] - temps[0] > band and len(temps)>2:
		if temps[1] - temps[0] > temps[-1] - temps[-2]:
			del temps[0]
		else:
			del temps[-1]

	if len(temps) > critical*length:
		qc[-1] = True

	return qc

def end_loose_loose_constant(p):
	# look for a critical fraction of points in the last span meters falling within a tight band
	t = p.t()
	z = p.z()
	span = 300
	band = 1
	critical = 0.9
	temps = []
	qc = [False]*len(t)

    # get last span worth of points
    # don't tolerate any nan
	i=1
	while z[-1] - z[-1*i] < span and i < len(t):
		if(math.isnan(t[-1*i])):
			return qc
		temps.append(t[-1*i])
		i+=1

	# only counts if this is sufficiently deep
	if z[-1*i] < 500:
		return qc

	length = len(temps)

    # eliminate furthest outliers until only a cluster within band remains
	temps.sort()
	while temps[-1] - temps[0] > band and len(temps)>2:
		if temps[1] - temps[0] > temps[-1] - temps[-2]:
			del temps[0]
		else:
			del temps[-1]

	if len(temps) > critical*length:
		qc[-1] = True

	return qc

def csiro_wire_break(p):
	# inspired by CSIRO's wire break test

    # Get temperature values from the profile.
    t = p.t()
    qc = [False]*len(t)

    # wire breaks at bottom of profile:
    if t[-1] < -2.8 or t[-1] > 36:
        qc[-1] = True

    return qc

def simple_gradient(p):

	t = p.t()
	z = p.z()
	qc = [False]*len(t)

	for i in range(len(t)-1):
		if t[i] == 99.99 or t[i+1] == 99.99:
			continue
		deltaZ = z[i+1] - z[i]
		deltaT = t[i+1] - t[i]
		if abs(deltaT / deltaZ) > 10:
			qc[i+1] = True

	return qc