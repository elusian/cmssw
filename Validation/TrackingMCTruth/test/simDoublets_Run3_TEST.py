"""
This script runs the SimDoubletsProducer and SimDoubletsAnalyzer.
It is just meant for testing and development.

!!! NOTE !!!
You have to change at least the input file for now.
"""

import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_2025_cff import Run3_2025

process = cms.Process("SIMDOUBLETS",Run3_2025)

# maximum number of events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

with open('ttbar_file_list.txt') as list_file:
    file_list = list_file.readlines()

# Input source
process.source = cms.Source("PoolSource",
    dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
    fileNames = cms.untracked.vstring(file_list),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_hltSiPixelRecHits_*_HLTX'   # we will reproduce them to have their local position available
    ),
    secondaryFileNames = cms.untracked.vstring()
)


### conditions
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '142X_mcRun3_2025_realistic_v4', '')

### standard includes
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.RawToDigi_cff")
process.load("Configuration.EventContent.EventContent_cff")
# process.load("Configuration.StandardSequences.Reconstruction_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

### load hltTPClusterProducer
process.load("Validation.RecoTrack.associators_cff")
### load the new EDProducer "SimDoubletsProducer"
process.load("SimTracker.TrackerHitAssociation.simDoubletsProducer_cfi")
### load the new DQM EDAnalyzer "SimDoubletsAnalyzer"
process.load("Validation.TrackingMCTruth.simDoubletsAnalyzer_cfi")

# process.HLTDoLocalPixelSequence = cms.Sequence(process.hltSiPixelRecHitsSoA + process.hltSiPixelRecHits)

####  set up the paths
process.simDoubletProduction = cms.Path(
    process.HLTDoLocalPixelSequence *
    process.hltTPClusterProducer *
    process.simDoubletsProducer *
    process.simDoubletsAnalyzer
)

process.simDoubletsAnalyzer.cellPhiCuts = [965, 1241, 395, 698, 1058, 1211, 348, 782, 1016, 810, 463, 755, 694, 531, 770, 471, 592, 750, 348]
process.simDoubletsAnalyzer.cellMinz = [-20., 0., -30., -22., 10., -30., -70., -70., -22., 15., -30, -70., -70., -20., -22., 0, -30., -70., -70.]
process.simDoubletsAnalyzer.cellMaxz = [20., 30., 0., 22., 30., -10., 70., 70., 22., 30., -15., 70., 70., 20., 22., 30., 0., 70., 70.]
process.simDoubletsAnalyzer.cellMaxr = [20., 9., 9., 20., 7., 7., 5., 5., 20., 6., 6., 5., 5., 20., 20., 9., 9., 9., 9.]
process.simDoubletsAnalyzer.cellPtCut = 0.5
process.simDoubletsAnalyzer.cellZ0Cut = 12
process.simDoubletsAnalyzer.cellMinYSizeB1 = 36
process.simDoubletsAnalyzer.cellMinYSizeB2 = 28
process.simDoubletsAnalyzer.cellMaxDYSize12 = 28
process.simDoubletsAnalyzer.cellMaxDYSize = 20;
process.simDoubletsAnalyzer.cellMaxDYPred = 20;

process.simDoubletsProducer.TrackingParticleSelectionConfig = cms.PSet(
    chargedOnly = cms.bool(True),
    intimeOnly = cms.bool(False),
    invertRapidityCut = cms.bool(False),
    lip = cms.double(30.0),
    maxPhi = cms.double(3.2),
    maxRapidity = cms.double(3),
    minHit = cms.int32(0),
    minPhi = cms.double(-3.2),
    minRapidity = cms.double(-3),
    pdgId = cms.vint32(),
    ptMax = cms.double(1e+100),
    ptMin = cms.double(0.9),
    signalOnly = cms.bool(True),
    stableOnly = cms.bool(False),
    tip = cms.double(60.0)
)

# Output definition
process.MyTestoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_simDoubletsProducer_*_SIMDOUBLETS'  # just keep the newly produced branches
    ),
    fileName = cms.untracked.string('file:simDoublets_TEST.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('TEST')
    )
)

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:simDoublets_TEST_DQMIO.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)


process.endjob_step = cms.EndPath(process.endOfProcess)
process.MyTestoutput_step = cms.EndPath(process.MyTestoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)


process.schedule = cms.Schedule(
      process.simDoubletProduction,process.endjob_step,process.MyTestoutput_step, process.DQMoutput_step
)

process.options = cms.untracked.PSet(
    numberOfThreads = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(1),
    wantSummary = cms.untracked.bool(True)
)
