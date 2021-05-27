def jerkcost(xjerktraj, MovementDur, framerate, max_vel, yjerktraj=None, zjerktraj=None):
    #calculate jerk cost
    import numpy
    if yacctraj and zacctraj:
       # print('3D Jerk')
       sumval = xjerktraj**2 + yjerktraj**2 + zjerktraj**2
    else:
       # print('2D Jerk')
       sumval = xjerktraj**2
    jerkcost_out = -numpy.log(abs(numpy.trapz(sumval)*1/framerate*MovementDur**3/max_vel**2))
    return jerkcost_out