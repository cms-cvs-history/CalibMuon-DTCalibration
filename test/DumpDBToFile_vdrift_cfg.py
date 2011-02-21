import FWCore.ParameterSet.Config as cms

from Utilities.PyConfigTools.parseInput import parseInput
inputFields = ('vDriftDB',)
inputOptions = parseInput(inputFields,requiredFields=inputFields)

process = cms.Process("DumpDBToFile")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(1)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.calibDB = cms.ESSource("PoolDBESSource",
    process.CondDBSetup,
    authenticationMethod = cms.untracked.uint32(0),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTMtimeRcd'),
        tag = cms.string('vDrift')
    )),
    connect = cms.string('sqlite_file:%s' % inputOptions.vDriftDB)
)

process.dumpToFile = cms.EDAnalyzer("DumpDBToFile",
    # Choose what database you want to write
    dbToDump = cms.untracked.string('VDriftDB'),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(5),
        # VDrift & TTrig
        calibConstGranularity = cms.untracked.string('bySL')
    ),
    outputFileName = cms.untracked.string('%s.txt' % inputOptions.vDriftDB.split('.')[0])
)

process.p = cms.Path(process.dumpToFile)