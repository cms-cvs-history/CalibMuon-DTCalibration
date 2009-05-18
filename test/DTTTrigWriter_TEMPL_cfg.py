import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.DTGeometry.dtGeometry_cfi")
process.DTGeometryESModule.applyAlignment = False


process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.DTMapping = cms.ESSource("PoolDBESSource",
            DBParameters = cms.PSet(
            messageLevel = cms.untracked.int32(0),
            authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
           ),
           timetype = cms.string('runnumber'),
           toGet = cms.VPSet(cms.PSet(
           record = cms.string('DTT0Rcd'),
           tag = cms.string('TZEROTEMPLATE')
           ),
           cms.PSet(
           record = cms.string('DTStatusFlagRcd'),
           tag = cms.string('NOISETEMPLATE')
           )),
          connect = cms.string('CMSCONDVSTEMPLATE'),
         siteLocalConfig = cms.untracked.bool(False)
     )
process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/ttrig_first_TEMPLATE.db'),
    authenticationMethod = cms.untracked.uint32(0),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    ))
)


process.load("CalibMuon.DTCalibration.DTTTrigWriter_cfi")
process.ttrigwriter.kFactor = -0.7
process.ttrigwriter.rootFileName = "/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/DTTimeBoxes_TEMPLATE.root"


process.p = cms.Path(process.ttrigwriter)


