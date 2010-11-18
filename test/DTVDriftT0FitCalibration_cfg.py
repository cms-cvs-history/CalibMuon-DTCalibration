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
process.GlobalTag.globaltag = "GR_R_38X_V14::All"

process.load("RecoLocalMuon.Configuration.RecoLocalMuon_cff")
process.dt2DSegments.Reco2DAlgoConfig.performT0_vdriftSegCorrection = True
process.dt4DSegments.Reco4DAlgoConfig.performT0_vdriftSegCorrection = True

process.load("EventFilter.DTRawToDigi.dtunpacker_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/data/Run2010B/Mu/RAW-RECO/v2/000/149/711/F67961F1-F0E7-DF11-A2C8-90E6BA19A22E.root',
        '/store/data/Run2010B/Mu/RAW-RECO/v2/000/149/709/C29F6BC9-DBE7-DF11-B1B4-E0CB4E19F9A6.root',
        '/store/data/Run2010B/Mu/RAW-RECO/v2/000/149/510/164F69F5-9FE7-DF11-9026-E0CB4E29C50B.root',
        '/store/data/Run2010B/Mu/RAW-RECO/v2/000/149/509/144B4A0E-4DE7-DF11-943B-485B39800C32.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.dtVDriftCalibration = cms.EDAnalyzer("DTVDriftT0FitCalibration",
    recHits4DLabel = cms.InputTag('dt4DSegments'),
    rootFileName = cms.untracked.string('/tmp/antoniov/DTVDriftHistos.root'),
    # Choose the chamber you want to calibrate (default = "All"), specify the chosen chamber
    # in the format "wheel station sector" (i.e. "-1 3 10")
    calibChamber = cms.untracked.string('All'),
    # Segment selection
    checkNoisyChannels = cms.bool(False),
    minHitsPhi = cms.int32(7),
    minHitsZ = cms.int32(4),
    maxChi2 = cms.double(1000.0),
    maxAnglePhi = cms.double(25.),
    maxAngleZ = cms.double(999.)
)

process.load("CalibMuon.DTCalibration.dtCalibOfflineSelection_cff")

process.p = cms.Path(process.dtCalibOfflineSelection+
                     process.muonDTDigis*
                     process.dt1DRecHits*process.dt2DSegments*process.dt4DSegments*
                     process.dtVDriftCalibration)
