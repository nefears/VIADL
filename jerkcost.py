def jerkcost(xjerktraj, movementdur, framerate, pathlength, yjerktraj=None, zjerktraj=None):
    #calculate jerk cost
    import numpy
    if yjerktraj and zjerktraj:
       # print('3D Jerk')
       sumval = xjerktraj**2 + yjerktraj**2 + zjerktraj**2
    else:
       # print('2D Jerk')
       sumval = xjerktraj**2
    # jerkcost_out = -numpy.log(abs(numpy.trapz(sumval) * 1/framerate * movementdur**5 / dist**2))
    jerkcost_out = numpy.log((movementdur**5/pathlength**2)*numpy.trapz(sumval)*(1/framerate))
    return jerkcost_out

