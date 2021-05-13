def jerkcost(x, frametime, framerate, max_vel, y=None, z=None):
    #calculate jerk cost
    import numpy
    if y and z:
       # print('3D Jerk')
       sumval = numpy.square(x) + numpy.square(y) + numpy.square(z)
    else:
       # print('2D Jerk')
       sumval = numpy.square(x)
    jerkcost_out = -numpy.log(abs(numpy.trapz(sumval)*1/framerate*frametime**3/max_vel**2))
    return jerkcost_out