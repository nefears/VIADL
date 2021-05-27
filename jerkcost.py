def jerkcost(xjerktraj, movementdur, framerate, dist, yjerktraj=None, zjerktraj=None):
    #calculate jerk cost
    import numpy
    if yjerktraj and zjerktraj:
       # print('3D Jerk')
       sumval = xjerktraj**2 + yjerktraj**2 + zjerktraj**2
    else:
       # print('2D Jerk')
       sumval = xjerktraj**2
    jerkcost_out = -numpy.log(abs(numpy.trapz(sumval) * 1/framerate * movementdur**5 / dist**2))
    #jerkcost_out = -numpy.log(abs(numpy.trapz(sumval)*1/framerate*movementdur**3/max_vel**2))  # velocity based from Ty's code
    return jerkcost_out