def jerkcost(x, y, z, frametime,framerate, max_vel):
    #calculate jerk cost
    import numpy
    if x and y and z:
        sumval=numpy.square(x) + numpy.square(y) + numpy.square(z)
    elif x:
        sumval = numpy.square(x)
    jerkcost_out = -numpy.log(abs(numpy.trapz(sumval)*1/framerate*frametime^3/max_vel^2))
    return jerkcost_out