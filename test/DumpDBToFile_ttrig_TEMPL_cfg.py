import FWCore.ParameterSet.Config as cms

process = cms.Process("DumpDBToFile")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(149442)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.get = cms.EDAnalyzer("DTTtrigPrint")

process.calibDB = cms.ESSource("PoolDBESSource",
    process.CondDBSetup,
    authenticationMethod = cms.untracked.uint32(0),
    toGet = cms.VPSet(cms.PSet(
        # VDrift
        #string record = "DTMtimeRcd"
        #string tag ="vDrift"
        # TZero
        #string record = "DTT0Rcd" 
        #string tag = "t0"
        #string tag = "t0_GRUMM"
        # TTrig
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('DT_tTrig_cosmics_2009_v3_prompt')
    )),
    connect = cms.string('frontier://FrontierProd/CMS_COND_31X_DT')
)

process.dumpToFile = cms.EDAnalyzer("DumpDBToFile",
    #Choose what database you want to write
    #untracked string dbToDump = "VDriftDB"
    #untracked string dbToDump = "TZeroDB"
    dbToDump = cms.untracked.string('TTrigDB'),
    dbLabel = cms.untracked.string(''),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(5),
        # VDrift & TTrig
        calibConstGranularity = cms.untracked.string('bySL')
    ),
    outputFileName = cms.untracked.string('ttrig_DT_tTrig_cosmics_2009_v3_prompt_149442.txt')
)

process.p = cms.Path(process.dumpToFile)
