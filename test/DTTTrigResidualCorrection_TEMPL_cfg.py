import FWCore.ParameterSet.Config as cms

process = cms.Process("DTTTrigCorrection")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.DTGeometry.dtGeometry_cfi")
process.DTGeometryESModule.applyAlignment = False

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")


process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.debugModules = cms.untracked.vstring('*')
process.MessageLogger.destinations = cms.untracked.vstring('cerr')
process.MessageLogger.categories.append('Calibration')
process.MessageLogger.cerr =  cms.untracked.PSet(
     threshold = cms.untracked.string('DEBUG'),
     noLineBreaks = cms.untracked.bool(False),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     INFO = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     Calibration = cms.untracked.PSet(limit = cms.untracked.int32(-1))
)

#process.load("Configuration.StandardSequences.Geometry_cff")
#process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cfi")
#process.GlobalTag.connect = "frontier://FrontierProd/CMS_COND_21X_GLOBALTAG"
#process.GlobalTag.globaltag = "CRAFT_ALL_V4::All"
process.DTMapping = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(
        cms.PSet(
        record = cms.string('DTReadOutMappingRcd'),
        tag = cms.string('MAPTEMPLATE')
        ),
        cms.PSet(
            record = cms.string('DTT0Rcd'),
            tag = cms.string('TZEROTEMPLATE')
        ), 
        cms.PSet(
            record = cms.string('DTStatusFlagRcd'),
            tag = cms.string('NOISETEMPLATE')
        ),
         cms.PSet(
            record = cms.string('DTMtimeRcd'),
            tag = cms.string('VDRIFTTEMPLATE')
        )       
     ),
     connect = cms.string('CMSCONDVSTEMPLATE'),
 #   connect = cms.string('frontier://FrontierProd/CMS_COND_30X_DT'),
    siteLocalConfig = cms.untracked.bool(False)
)
 
#process.load("CalibMuon.DTCalibration.dt_DBLocal_cff")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.ttrig = cms.ESSource("PoolDBESSource",
    process.CondDBSetup,
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    )),
    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/ttrig_second_RUNNUMBERTEMPLATE.db'),
    authenticationMethod = cms.untracked.uint32(0)
)

#process.es_prefer_calibDB = cms.ESPrefer('PoolDBESSource','ttrig')

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    process.CondDBSetup,
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/ttrig_ResidCorr_RUNNUMBERTEMPLATE.db'),
    authenticationMethod = cms.untracked.uint32(0),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    ))
)

process.DTTTrigCorrection = cms.EDAnalyzer("DTTTrigCorrection",
    correctionAlgo = cms.string('DTTTrigResidualCorrection'),
    correctionAlgoConfig = cms.PSet(
        residualsRootFile = cms.string('/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/RUNPERIODTEMPL/ttrig/DTkFactValidation_RUNNUMBERTEMPLATE.root'),
        useFitToResiduals = cms.bool(True)
    )
)

process.p = cms.Path(process.DTTTrigCorrection)


