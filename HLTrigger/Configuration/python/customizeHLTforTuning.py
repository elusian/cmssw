
import FWCore.ParameterSet.Config as cms

def customizeHLTForTuning15(process):
    row = [1.18672346e-03, 2.09774178e-03, 2.98055573e-02, 6.01157831e-01,
           3.77946519e-01, 8.95719315e+00, 6.44085859e+02, 5.65163412e+02,
           5.83529900e+02, 7.06934467e+02, 7.13556878e+02, 8.29831408e+02,
           6.55924557e+02, 8.33180168e+02, 6.89859010e+02, 4.35916983e+02,
           6.36339946e+02, 7.56984834e+02, 7.04178219e+02, 6.53876411e+02,
           6.42245253e+02, 6.11439625e+02, 6.65703855e+02, 7.69764317e+02,
           7.97232498e+02]

    for module in [process.hltPixelTracksGPU, process.hltPixelTracksCPU, process.hltPixelTracksCPUOnly]:
        module.CAThetaCutBarrel = cms.double(float(row[0]))
        module.CAThetaCutForward = cms.double(float(row[1]))
        module.dcaCutInnerTriplet = cms.double(float(row[2]))
        module.dcaCutOuterTriplet = cms.double(float(row[3]))
        module.hardCurvCut = cms.double(float(row[4]))
        module.z0Cut = cms.double(float(row[5]))
        module.phiCuts = cms.vint32(
            int(row[6]), int(row[7]), int(row[8]), int(row[9]), int(row[10]),
            int(row[11]), int(row[12]), int(row[13]), int(row[14]), int(row[15]),
            int(row[16]), int(row[17]), int(row[18]), int(row[19]), int(row[20]),
            int(row[21]), int(row[22]), int(row[23]), int(row[24])
        )
    return process
