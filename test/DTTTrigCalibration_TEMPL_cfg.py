# The following comments couldn't be translated into the new config version:

#Service to write DB if ttrigcalib.findTMeanAndSigma is true

import FWCore.ParameterSet.Config as cms

process = cms.Process("TTRIGCALIBPROC")

process.load("Configuration.StandardSequences.Geometry_cff")


process.load("FrontierConditions_GlobalTag_noesprefer_cff")
process.GlobalTag.globaltag = "CRAFT_V2P::All"

process.dtDBPrefer = cms.ESPrefer("PoolDBESSource","DTMapping")


process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("PoolSource",
    useCSA08Kludge = cms.untracked.bool(True),
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)


process.load("CalibMuon.DTCalibration.DTTTrigCalibration_cfi")
process.ttrigcalib.rootFileName = 'DTTimeBoxes.root'
process.ttrigcalib.kFactor = -0.7

# if read from RAW
#process.ttrigcalib.digiLabel = 'dtunpacker'
#process.load("EventFilter.DTRawToDigi.dtunpacker_cfi")

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
    connect = cms.string('oracle://cms_orcoff_prod/CMSCONDVSTEMPLATE'),
    #        string connect = "frontier://FrontierOn/CMS_COND_ON_18X_DT"
    siteLocalConfig = cms.untracked.bool(False)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    authenticationMethod = cms.untracked.uint32(0),
    connect = cms.string('sqlite_file:ttrig.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    ))
)

process.p = cms.Path(process.ttrigcalib)

# if read from RAW
#process.p = cms.Path(process.muonDTDigis*process.ttrigcalib)
