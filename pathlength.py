def pathlength(StartRow, EndRow, MarkerX, MarkerY, MarkerZ):
    import numpy
    if 'MarkerX':
        XPathLength=sum(abs(numpy.diff(MarkerX[StartRow:EndRow])))
    if 'MarkerY':
        YPathLength=sum(abs(numpy.diff(MarkerY[StartRow:EndRow])))
    if 'MarkerZ':
        ZPathLength=sum(abs(numpy.diff(MarkerZ[StartRow:EndRow])))
    if 'MarkerX' and 'MarkerY' and 'MarkerZ':
        markers = numpy.asarray(list(zip(MarkerX[StartRow:EndRow], MarkerY[StartRow:EndRow], MarkerZ[StartRow:EndRow])))
        ThreeDPathLength = 0
        for pt1, pt2 in zip(markers, markers[1:]):
            ThreeDPathLength += abs(numpy.linalg.norm(pt2-pt1, 2))
    return XPathLength, YPathLength, ZPathLength, ThreeDPathLength
