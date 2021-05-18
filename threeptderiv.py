def threeptderiv(StartRow, EndRow, data, frametime, filter_order, filter_cutoff, filter_type):
    # Calculate numerical three point derivative for most points, two point derivative for first and last points
    import numpy
    from scipy import signal
    midStartPoint = StartRow+1 # start point needed to stay within bounds of array
    midEndPoint = EndRow # end point needed to stay within bounds of array
    deriv=numpy.empty([1,0]) # empy numpy.array to collect data
    # calculate three point derivative for mid points of dataset
    for pt1, pt2 in zip(data[midStartPoint + 1:midEndPoint + 1], data[midStartPoint - 1:midEndPoint - 1]):
        deriv = numpy.append(deriv, ((pt1 - pt2) / (2 * frametime)))
        # print(pt1, pt2)
        # print(deriv)
    # calculate two point derivative for first and last frames
    firstpoint = (data[1]-data[0])/frametime
    lastpoint = (data[len(data)-1]-data[len(data)-2])/frametime
    deriv = numpy.append(firstpoint, deriv)
    # print(data[1], data[0])
    # print(deriv)
    deriv = numpy.append(deriv, lastpoint)
    # print(data[len(data)-1], data[len(data)-2])
    # print(deriv)
    if filter_order and filter_type and filter_type:
        b, a = signal.butter(filter_order, filter_cutoff, filter_type)
        deriv_out = signal.filtfilt(b, a, deriv)
    return deriv_out