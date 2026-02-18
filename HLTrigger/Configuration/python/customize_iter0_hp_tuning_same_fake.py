
from collections.abc import Iterable
def assign(target, val):
    if isinstance(target, Iterable):
        target[2] = val
    else:
        target = val

def customize_for_hp_tuning(process):
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.d0err, 0.003968462793686334)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.d0err_par, 0.000118143034192274)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_exp, int(2.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par1, 1.1563859327766106)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par2, 0.8431723014309169)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_exp, int(2.6748437953689503))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par1, 1.2501966670755764)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par2, 0.6042645354699189)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxChi2, 857.0958554215441)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxChi2n, 954.4857184737727)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxLostLayers, int(-0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.min3DLayers, int(-0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minLayers, int(0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minNVtxTrk, int(1.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minNdof, 0.0)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minPixelHits, int(2.0))
    return process
