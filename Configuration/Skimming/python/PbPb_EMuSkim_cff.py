import FWCore.ParameterSet.Config as cms

# Electron or muon HLT trigger
import HLTrigger.HLTfilters.hltHighLevel_cfi
hltEMuHI = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
hltEMuHI.HLTPaths = ["HLT_HIEle*Gsf_v*","HLT_HIL2SingleMu*_v*","HLT_HIL3SingleMu*_v*"]
hltEMuHI.throw = False
hltEMuHI.andOr = True

# selection of valid vertex
primaryVertexFilterForEMu = cms.EDFilter("VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake && abs(z) <= 25 && position.Rho <= 2"), 
    filter = cms.bool(True),   # otherwise it won't filter the events
    )

# single lepton selector                                                                                                                                               
electronSelectorForEMu = cms.EDFilter("GsfElectronRefSelector",
                                   src = cms.InputTag("gedGsfElectrons"),
                                   cut = cms.string("pt > 20")
                                   )

muonSelectorForEMu = cms.EDFilter("MuonSelector",
                                  src = cms.InputTag("muons"),
                                  cut = cms.string("isPFMuon && isGlobalMuon && pt > 20. && abs(eta)<2.4 && (globalTrack().normalizedChi2() < 10) && (globalTrack().hitPattern().numberOfValidMuonHits()>0) && (numberOfMatchedStations() > 1)"),
                                  filter = cms.bool(True)
    )


# EMu skim sequence
emuSkimSequence = cms.Sequence(
    hltEMuHI *
    primaryVertexFilterForEMu *
    electronSelectorForEMu * 
    muonSelectorForEMu
)
