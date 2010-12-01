import FWCore.ParameterSet.Config as cms

process = cms.Process("Calibration")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.debugModules = cms.untracked.vstring('dtVDriftCalibration')
process.MessageLogger.destinations = cms.untracked.vstring('cerr')
process.MessageLogger.categories.append('Calibration')
process.MessageLogger.cerr =  cms.untracked.PSet(
     threshold = cms.untracked.string('DEBUG'),
     noLineBreaks = cms.untracked.bool(False),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     INFO = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     Calibration = cms.untracked.PSet(limit = cms.untracked.int32(-1))
)

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "FT_R_38X_V14A::All"

process.load("RecoLocalMuon.Configuration.RecoLocalMuon_cff")

process.load("EventFilter.DTRawToDigi.dtunpacker_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
    lumisToProcess = cms.untracked.VLuminosityBlockRange()
)
#from fileNames_WZSkim_Mu_Run2010B_WZMuFilter_v2 import fileNames as fileNamesWZ
#from fileNames_WZSkim_Mu_Run2010B_WZMu_v2 import fileNames as fileNamesWZ
from fileNames_Mu_Run2010B_WZMu_Nov4Skim_v1 import fileNames
process.source.fileNames = fileNames 
#from lumisToProcess_136033_149442_7TeV_Nov4ReReco_MuonPhys import lumisToProcess
from lumisToProcess_144045_149442_7TeV_Nov4ReReco_MuonPhys import lumisToProcess
process.source.lumisToProcess = lumisToProcess

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.dtVDriftCalibration = cms.EDAnalyzer("DTVDriftCalibration",
    recHits4DLabel = cms.InputTag('dt4DSegments'), 
    rootFileName = cms.untracked.string('DTTMaxHistos.root'),
    # Choose the chamber you want to calibrate (default = "All"), specify the chosen chamber
    # in the format "wheel station sector" (i.e. "-1 3 10")
    calibChamber = cms.untracked.string('All'),
    debug = cms.untracked.bool(False),
    # Segment selection
    checkNoisyChannels = cms.bool(False),
    minHitsPhi = cms.int32(7),
    minHitsZ = cms.int32(4),
    maxChi2 = cms.double(1000.0),
    maxAnglePhi = cms.double(25.),
    maxAngleZ = cms.double(999.),
    # Chosen granularity (N.B. bySL is the only one implemented at the moment)  
    tMaxGranularity = cms.untracked.string('bySL'),
    # The module to be used for ttrig synchronization and its set parameter
    tTrigMode = cms.string('DTTTrigSyncFromDB'),
    tTrigModeConfig = cms.PSet(
        # The velocity of signal propagation along the wire (cm/ns)
        vPropWire = cms.double(24.4),
        # Switch on/off the TOF correction for particles
        doTOFCorrection = cms.bool(True),
        tofCorrType = cms.int32(0),
        wirePropCorrType = cms.int32(0),
        # Switch on/off the correction for the signal propagation along the wire
        doWirePropCorrection = cms.bool(True),
        # Switch on/off the TO correction from pulses
        doT0Correction = cms.bool(True),
        debug = cms.untracked.bool(False),
        tTrigLabel = cms.string('')
    ),
    # Choose to calculate vDrift and t0 or just fill the TMax histograms
    findVDriftAndT0 = cms.untracked.bool(False),
    # Parameter set for DTCalibrationMap constructor
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(6),
        calibConstGranularity = cms.untracked.string('bySL'),
        calibConstFileName = cms.untracked.string('vDriftAndReso.txt')
    ),
    # Name of the txt file which will contain the calibrated v_drift
    vDriftFileName = cms.untracked.string('vDrift_fromMtime.txt')
)

process.load("CalibMuon.DTCalibration.dtCalibOfflineSelection_cff")

process.p = cms.Path(process.dtCalibOfflineSelection+
                     process.muonDTDigis*
                     process.dt1DRecHits*process.dt2DSegments*process.dt4DSegments*
                     process.dtVDriftCalibration)
