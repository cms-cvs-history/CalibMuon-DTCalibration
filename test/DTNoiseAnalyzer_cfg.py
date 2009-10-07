import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "GR09_P_V1::All"

process.load("CondCore.DBCommon.CondDBSetup_cfi")

#process.load("DQMServices.Core.DQM_cfg")


process.source = cms.Source("PoolSource",
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring(

       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/113/222/14019B7F-8899-DE11-8FCE-000423D9853C.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/700/BAFDDC41-2F97-DE11-B9F4-000423D6CA02.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/698/B0C9C9D4-4797-DE11-9CA1-000423D992DC.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/698/4AF66DC5-3297-DE11-ADF3-001617C3B710.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/D443105E-2A97-DE11-9936-000423DD2F34.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/B86FFDF2-4297-DE11-B14E-000423D99996.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/A4199619-9397-DE11-AF8B-001617DBD556.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/84FC8A38-6198-DE11-94C7-000423D6AF24.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/5812A978-1498-DE11-B65E-000423D6CA6E.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/4E9A833D-2F97-DE11-A21A-001617E30CE8.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/462706ED-C797-DE11-9C70-001617E30CD4.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/697/44DBD5B2-BC97-DE11-B845-001617C3B710.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/9C54D13E-2897-DE11-B675-000423D9863C.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/78238060-2A97-DE11-8CDF-000423D992DC.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/5ACEB933-3B97-DE11-87AD-000423D6B5C4.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/52FE243D-2197-DE11-BAAC-0016177CA7A0.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/38727227-2697-DE11-94CF-001617C3B6CE.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/691/321A4BFF-2397-DE11-A054-000423D6AF24.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/686/C8C8AB3B-1A97-DE11-999B-001D09F29849.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/686/1CEB9C08-1D97-DE11-B503-00304879FBB2.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/686/08DEF4E2-1A97-DE11-8602-0016177CA7A0.root',
       '/store/express/CRAFT09/StreamExpress/ALCARECO/v1/000/112/650/C0A93535-F596-DE11-A43E-000423D985B0.root'



    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100000)
)


# if read from RAW
#process.load("EventFilter.DTRawToDigi.dtunpacker_cfi")

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    authenticationMethod = cms.untracked.uint32(0),
    connect = cms.string('sqlite_file:noise.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTStatusFlagRcd'),
        tag = cms.string('noise')
    ))
)

process.noiseCalib = cms.EDFilter("DTNoiseCalibration",
    #Define the wheel of interest (to set if fastAnalysis=false)
    wheel = cms.untracked.int32(0),
    #Define the sector of interest (to set if fastAnalysis=false)
    sector = cms.untracked.int32(11),
    #Database option (to set if cosmicRun=true)
    readDB = cms.untracked.bool(True),
    #The trigger width(TDC counts) (to set if cosmicRun=true and readDB=false)
    defaultTtrig = cms.untracked.int32(400),
    fastAnalysis = cms.untracked.bool(True),
    rootFileName = cms.untracked.string('DTNoiseCalib.root'),
    # Label to retrieve DT digis from the event
    # RAW: dtunpacker DIGI: muonDTDigis
    digiLabel = cms.untracked.string('muonDTDigis'), 
    #Trigger mode
    cosmicRun = cms.untracked.bool(True),
    debug = cms.untracked.bool(False),
    #The trigger width(ns) (to set if cosmicRun=false)
    TriggerWidth = cms.untracked.int32(25350),
    theOffset = cms.untracked.double(100.)
)

process.noiseComp = cms.EDFilter("DTNoiseComputation",
    debug = cms.untracked.bool(False),
    fastAnalysis = cms.untracked.bool(False),
    #Total number of events	
    MaxEvents = cms.untracked.int32(200000),
    rootFileName = cms.untracked.string('DTNoiseCalib.root'),
    #Name of the ROOT file which will contains the
    newRootFileName = cms.untracked.string('DTNoiseComp.root')
)

#process.p = cms.Path(process.dtunpacker*process.noiseCalib)

process.p = cms.Path(process.noiseCalib)


