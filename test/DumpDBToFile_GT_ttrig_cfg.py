import FWCore.ParameterSet.Config as cms
import sys,os

run = None
globaltag = None
for k in sys.argv:
    if k[:4] == 'run=': run = k[4:]
    if k[:10] == 'globaltag=': globaltag = k[10:]

if not run: raise RuntimeError,'Need to set Run argument --> run='
if not globaltag: raise RuntimeError,'Need to set Globa Tag argument --> globaltag='

outfiletxt = 'ttrig_%s_%s.txt' % (globaltag.split('::')[0],run)

print "Using Run",run,"Global Tag",globaltag
print "Output file",outfiletxt

process = cms.Process("DumpDBToFile")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = globaltag + '::All'
if globaltag.find("_H_") != -1:
    process.GlobalTag.connect   = 'frontier://FrontierProd/CMS_COND_31X_GLOBALTAG'
    process.GlobalTag.pfnPrefix = cms.untracked.string('frontier://FrontierProd/')

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource",
    numberEventsInRun = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(int(run))
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.get = cms.EDFilter("DTTtrigPrint")

#process.calibDB = cms.ESSource("PoolDBESSource",
#    process.CondDBSetup,
#    authenticationMethod = cms.untracked.uint32(0),
#    toGet = cms.VPSet(cms.PSet(
#        # VDrift
#        #string record = "DTMtimeRcd"
#        #string tag ="vDrift"
#        # TZero
#        #string record = "DTT0Rcd" 
#        #string tag = "t0"
#        #string tag = "t0_GRUMM"
#        # TTrig
#        record = cms.string('DTTtrigRcd'),
#        tag = cms.string('ttrig')
#    )),
#    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/ttrig_DUMPDBTEMPL_RUNNUMBERTEMPLATE.db')
#)

process.dumpToFile = cms.EDAnalyzer("DumpDBToFile",
    #Choose what database you want to write
    #untracked string dbToDump = "VDriftDB"
    #untracked string dbToDump = "TZeroDB"
    dbToDump = cms.untracked.string('TTrigDB'),
    calibFileConfig = cms.untracked.PSet(
        nFields = cms.untracked.int32(5),
        # VDrift & TTrig
        calibConstGranularity = cms.untracked.string('bySL')
    ),
    outputFileName = cms.untracked.string(outfiletxt)
)

process.p = cms.Path(process.dumpToFile)
