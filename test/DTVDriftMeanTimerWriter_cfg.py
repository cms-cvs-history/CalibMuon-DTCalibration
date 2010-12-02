import FWCore.ParameterSet.Config as cms

class config: pass
#config.dtTMaxHistosFileName = 'DTTMaxHistos_144045_149442_7TeV_Nov4ReReco_MuonPhys.root'
config.dtTMaxHistosFileName = 'DTTMaxHistos_144045_149442_7TeV_Nov4ReReco_MuonPhys_newTTrig.root'
config.runNumber = 149442

process = cms.Process("DTVDriftWriter")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.debugModules = cms.untracked.vstring('dtVDriftWriter')
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
process.GlobalTag.globaltag = 'FT_R_38X_V14A::All'

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(config.runNumber)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBSetup,
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:vDrift.db'),
    authenticationMethod = cms.untracked.uint32(0),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTMtimeRcd'),
        tag = cms.string('vDrift')
    ))
)

process.dtVDriftWriter = cms.EDAnalyzer("DTVDriftWriter",
    vDriftAlgo = cms.string('DTVDriftMeanTimer'),
    vDriftAlgoConfig = cms.PSet(
        rootFileName = cms.string(config.dtTMaxHistosFileName),
        debug = cms.untracked.bool(True)
    )
)

process.p = cms.Path(process.dtVDriftWriter)
