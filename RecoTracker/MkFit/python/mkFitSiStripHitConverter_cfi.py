import FWCore.ParameterSet.Config as cms

from RecoTracker.MkFit.mkFitSiStripHitConverterDefault_cfi import mkFitSiStripHitConverterDefault as _mkFitSiStripHitConverterDefault
from RecoTracker.MkFit.mkFitSiStripHitConverterFromClustersDefault_cfi import mkFitSiStripHitConverterFromClustersDefault as _mkFitSiStripHitConverterFromClustersDefault
from RecoLocalTracker.SiStripClusterizer.SiStripClusterChargeCut_cfi import *

mkFitSiStripHitConverter = _mkFitSiStripHitConverterDefault.clone(
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('SiStripClusterChargeCutLoose'))
)
mkFitSiStripHitConverterFromClusters = _mkFitSiStripHitConverterFromClustersDefault.clone(
    minGoodStripCharge = cms.PSet(
        refToPSet_ = cms.string('SiStripClusterChargeCutLoose'))
)
