def pathlength(StartRow, EndRow, MarkerX, MarkerY, MarkerZ):
    if 'MarkerX':
        XPathLength=abs(diff(MarkerX[StartRow:EndRow+1]))
    if 'MarkerY':
        YPathLength=abs(diff(MarkerY[StartRow:EndRow+1]))
    if 'MarkerZ':
        ZPathLength=abs(diff(MarkerZ[StartRow:EndRow+1]))
    if 'MarkerX' and 'MarkerY' and 'MarkerZ':
        markers=[MarkerX, MarkerY, MarkerZ]
        ThreeDPathLength=


    return XPathLength, YPathLength, ZPathLength, ThreeDPathLength

