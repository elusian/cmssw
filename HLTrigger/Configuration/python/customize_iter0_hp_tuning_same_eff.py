
from collections.abc import Iterable
def assign(target, val):
    if isinstance(target, Iterable):
        target[2] = val
    else:
        target = val

def customize_for_hp_tuning(process):
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.d0err, 0.005165352354919935)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.d0err_par, 0.0001)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_exp, int(2.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par1, 0.9266575969713637)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dr_par.dr_par2, 0.5464433604281499)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_exp, int(2.141980877408618))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par1, 0.6507927779032667)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.dz_par.dz_par2, 0.4910039315424731)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxChi2, 1000.0)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxChi2n, 1000.0)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.maxLostLayers, int(0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.min3DLayers, int(0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minLayers, int(0.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minNVtxTrk, int(3.0))
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minNdof, 1.0)
    assign(process.hltIter0PFlowTrackCutClassifier.mva.minPixelHits, int(3.0))
    return process
