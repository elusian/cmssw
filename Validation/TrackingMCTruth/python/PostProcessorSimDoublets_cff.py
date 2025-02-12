import FWCore.ParameterSet.Config as cms
from DQMServices.Core.DQMEDHarvester import DQMEDHarvester
from Configuration.Eras.Modifier_fastSim_cff import fastSim

def _addNoFlow(module):
    _noflowSeen = set()
    for eff in module.efficiency.value():
        tmp = eff.split(" ")
        if "cut" in tmp[0]:
            continue
        ind = -1
        if tmp[ind] == "fake" or tmp[ind] == "simpleratio":
            ind = -2
        if not tmp[ind] in _noflowSeen:
            module.noFlowDists.append(tmp[ind])
        if not tmp[ind-1] in _noflowSeen:
            module.noFlowDists.append(tmp[ind-1])

_defaultSubdirs = ["Tracking/TrackingMCTruth/SimDoublets"]

postProcessorSimDoublets = DQMEDHarvester("DQMGenericClient",
    subDirs = cms.untracked.vstring(_defaultSubdirs),
    efficiency = cms.vstring(
        "efficiency_vs_pT 'SimDoublets efficiency per TP vs p_{T}; TP transverse momentum p_{T} [GeV]; Average fraction of SimDoublets per TP passing all cuts' numPassVsPt numTPTotVsPt",
        "efficiency_vs_eta 'SimDoublets efficiency vs #eta; TP pseudorapidity #eta; Average fraction of SimDoublets per TP passing all cuts' numPassVsEta numTPTotVsEta",
        "efficiencyTP_vs_pT 'TrackingParticle efficiency (2 or more connected SimDoublets passing cuts); TP transverse momentum p_{T} [GeV]; Efficiency for TrackingParticles' numTPPassVsPt numTPTotVsPt",
        "efficiencyTP_vs_eta 'TrackingParticle efficiency (2 or more connected SimDoublets passing cuts); TP pseudorapidity #eta; Efficiency for TrackingParticles' numTPPassVsEta numTPTotVsEta"
    ),
    resolution = cms.vstring(),
    cumulativeDists = cms.untracked.vstring(),
    noFlowDists = cms.untracked.vstring(),
    outputFileName = cms.untracked.string("")
)

_addNoFlow(postProcessorSimDoublets)
