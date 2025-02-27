import os
import FWCore.ParameterSet.Config as cms

#
# --- [cosmic sequence (default=True)?]
iscosmics = 'True'
print('iscosmics (default=True) = '+str(iscosmics))
# --- [name of job & output file (default=test)?]
jobname = 'test'
print('jobname (default=test) = '+str(jobname))
#
# --- [number of events (default=1000)]
nevents = 1000
print('nevents (default=1000)  = '+str(nevents))
#
# --- [turn on all histograms (default=True)?]
allhist = 'True'
print('allhist (default=True) = '+str(allhist))
#
#--- [trigger set (default=HLT)]
trigger_set = 'HLT'
print('trigger set name (default=HLT) = '+str(trigger_set))

#-----
process = cms.Process("test")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

#
# DQM
#
process.load("DQMServices.Core.DQM_cfg")

process.load("DQMServices.Components.MEtoEDMConverter_cfi")

#
# HCALNoise module
#
process.load("RecoMET.METProducers.hcalnoiseinfoproducer_cfi")
process.hcalnoise.refillRefVectors = cms.bool(True)
process.hcalnoise.hcalNoiseRBXCollName = "hcalnoise"
process.hcalnoise.requirePedestals = cms.bool(False)

#
# BeamHaloData producer
#
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration/StandardSequences/MagneticField_cff")
process.load("Configuration/StandardSequences/FrontierConditions_GlobalTag_cff")
process.load("RecoMET/Configuration/RecoMET_BeamHaloId_cff")
process.GlobalTag.globaltag ='GR09_R_34X_V2::All'

# the task - JetMET objects
if iscosmics =="True":
  process.load("DQMOffline.JetMET.jetMETDQMOfflineSourceCosmic_cff")
else:
  process.load("DQMOffline.JetMET.jetMETDQMOfflineSource_cff")

process.jetMETAnalyzer.OutputMEsInRootFile = cms.bool(True)
process.jetMETAnalyzer.OutputFileName = cms.string("jetMETMonitoring_test.root")
process.jetMETAnalyzer.TriggerResultsLabel = cms.InputTag("TriggerResults","",trigger_set)
process.jetMETAnalyzer.processname = cms.string(trigger_set)

if allhist=="True":
  process.jetMETAnalyzer.DoJetPtAnalysis = cms.untracked.bool(True)
  process.jetMETAnalyzer.DoJetPtCleaning = cms.untracked.bool(True)
  process.jetMETAnalyzer.DoIterativeCone = cms.untracked.bool(True)

process.jetMETAnalyzer.caloMETAnalysis.verbose = cms.int32(0)

if allhist=="True":
  process.jetMETAnalyzer.caloMETAnalysis.allSelection       = cms.bool(True)
  process.jetMETAnalyzer.caloMETNoHFAnalysis.allSelection   = cms.bool(True)
  process.jetMETAnalyzer.caloMETHOAnalysis.allSelection     = cms.bool(True)
  process.jetMETAnalyzer.caloMETNoHFHOAnalysis.allSelection = cms.bool(True)
  process.jetMETAnalyzer.pfMETAnalysis.allSelection         = cms.bool(True)
  process.jetMETAnalyzer.tcMETAnalysis.allSelection         = cms.bool(True)
  process.jetMETAnalyzer.mucorrMETAnalysis.allSelection     = cms.bool(True)

# the task - JetMET trigger
process.load("DQMOffline.Trigger.JetMETHLTOfflineSource_cfi")

# check # of bins
process.load("DQMServices.Components.DQMStoreStats_cfi")

# for igprof
#process.IgProfService = cms.Service("IgProfService",
#  reportFirstEvent            = cms.untracked.int32(0),
#  reportEventInterval         = cms.untracked.int32(25),
#  reportToFileAtPostEvent     = cms.untracked.string("| gzip -c > igdqm.%I.gz")
#)

#
# /Wmunu/Summer09-MC_31X_V3-v1/GEN-SIM-RECO
#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(*inputfiles))

#Load files from text
#import FWCore.Python.FileUtils as FileUtils
import FWCore.Utilities.FileUtils as FileUtils
readFiles = cms.untracked.vstring( FileUtils.loadListFromFile ('filelist_ExpressPhysics_121964.txt') )

#Extend the list if needed...
#readFiles.extend( FileUtils.loadListFromFile ('moreInfoIwant.txt') )

#Read the input files
process.source = cms.Source ("PoolSource",fileNames = readFiles)

#
process.source.inputCommands = cms.untracked.vstring('keep *', 'drop *_MEtoEDMConverter_*_*')
#
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( nevents )
)
process.Timing = cms.Service("Timing")

## # Comment this out or reconfigure to see error messages 
process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('jetMETAnalyzer'),
    cout = cms.untracked.PSet(
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        jetMETAnalyzer = cms.untracked.PSet(
            limit = cms.untracked.int32(100)
        ),
        noLineBreaks = cms.untracked.bool(True),
        DEBUG = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        threshold = cms.untracked.string('DEBUG')
    ),
    categories = cms.untracked.vstring('jetMETAnalyzer'),
    destinations = cms.untracked.vstring('cout')
)


process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.FEVT = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *_MEtoEDMConverter_*_*'),
    #outputCommands = cms.untracked.vstring('keep *'),
    fileName = cms.untracked.string("reco_DQM_test.root")
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True) ## default is false

)

if iscosmics=="True":
  process.p = cms.Path(process.hcalnoise
                       * process.BeamHaloId
                       * process.jetMETHLTOfflineSource
                       #                    * process.jetMETDQMOfflineSource
                       * process.jetMETDQMOfflineSourceCosmic
                       * process.MEtoEDMConverter
                       * process.dqmStoreStats)
else:
  process.p = cms.Path(process.hcalnoise
                       * process.BeamHaloId
                       * process.jetMETHLTOfflineSource
                       * process.jetMETDQMOfflineSource
                       #                    * process.jetMETDQMOfflineSourceCosmic
                       * process.MEtoEDMConverter
                       * process.dqmStoreStats)
  
process.outpath = cms.EndPath(process.FEVT)
process.DQM.collectorHost = ''

