def pathlength(StartRow, EndRow, MarkerX, MarkerY, MarkerZ):
    import numpy
    if 'MarkerX':
        XPathLength=sum(abs(numpy.diff(MarkerX)))
    if 'MarkerY':
        YPathLength=sum(abs(numpy.diff(MarkerY)))
    if 'MarkerZ':
        ZPathLength=sum(abs(numpy.diff(MarkerZ)))
    if 'MarkerX' and 'MarkerY' and 'MarkerZ':
        markers = numpy.asarray(list(zip(MarkerX, MarkerY, MarkerZ)))
        ThreeDPathLength = sum(abs(numpy.linalg.norm(pt2-pt1))
                             for pt1, pt2 in zip(markers, markers[1:]))
    return XPathLength, YPathLength, ZPathLength, ThreeDPathLength

