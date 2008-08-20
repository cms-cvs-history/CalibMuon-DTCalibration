# The following comments couldn't be translated into the new config version:

#tTrig (you need this database only if you run with cosmicRun=true and readDB=true)
# Noisy channels into DB

import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Geometry.MuonCommonData.muonIdealGeometryXML_cfi")

process.load("Geometry.DTGeometry.dtGeometry_cfi")
process.DTGeometryESModule.applyAlignment = False

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

from CalibTracker.Configuration.Common.PoolDBESSource_cfi import poolDBESSource
poolDBESSource.connect = "frontier://FrontierDev/CMS_COND_ALIGNMENT"
poolDBESSource.toGet = cms.VPSet(cms.PSet(
        record = cms.string('GlobalPositionRcd'),
        tag = cms.string('IdealGeometry')
    ))

process.load("FWCore.MessageService.MessageLogger_cfi")

process.source = cms.Source("PoolSource",
    useCSA08Kludge = cms.untracked.bool(True),
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring(
    '/store/data/Commissioning08/BarrelMuon/RAW/MW31_v1/000/053/517/3CC5C75F-115F-DD11-BA19-000423D98DB4.root',
    '/store/data/Commissioning08/BarrelMuon/RAW/MW31_v1/000/053/517/FE67DD23-0F5F-DD11-9180-001617C3B6FE.root'
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1000)
)
process.dtunpacker = cms.EDFilter("DTUnpackingModule",
    dataType = cms.string('DDU'),
    useStandardFEDid = cms.untracked.bool(True),
    fedbyType = cms.untracked.bool(True),
    readOutParameters = cms.PSet(
        debug = cms.untracked.bool(False),
        rosParameters = cms.PSet(
            writeSC = cms.untracked.bool(True),
            readingDDU = cms.untracked.bool(True),
            performDataIntegrityMonitor = cms.untracked.bool(False),
            readDDUIDfromDDU = cms.untracked.bool(True),
            debug = cms.untracked.bool(False),
            localDAQ = cms.untracked.bool(False)
        ),
        localDAQ = cms.untracked.bool(False),
        performDataIntegrityMonitor = cms.untracked.bool(False)
    )
)

process.DTMapping = cms.ESSource("PoolDBESSource",
    DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0),
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTReadOutMappingRcd'),
        tag = cms.string('map_CRUZET'),
        ),
        cms.PSet(
            record = cms.string('DTTtrigRcd'),
            tag = cms.string('tTrig_CRUZET_080708_2019')
    )),
    connect = cms.string('frontier://FrontierProd/CMS_COND_20X_DT'),
    siteLocalConfig = cms.untracked.bool(False)
)

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
    fastAnalysis = cms.untracked.bool(True),
    rootFileName = cms.untracked.string('DTNoiseCalib.root'),
    debug = cms.untracked.bool(False),
    #Trigger mode
    cosmicRun = cms.untracked.bool(True),
    #Define the wheel of interest (to set if fastAnalysis=false)
    wheel = cms.untracked.int32(0),
    #Define the sector of interest (to set if fastAnalysis=false)
    sector = cms.untracked.int32(11),
    #Database option (to set if cosmicRun=true)
    readDB = cms.untracked.bool(True),
    #The trigger width(TDC counts) (to set if cosmicRun=true and readDB=false)
    defaultTtrig = cms.untracked.int32(2800),
    #The trigger width(ns) (to set if cosmicRun=false)
    TriggerWidth = cms.untracked.int32(25350)
)

process.noiseComp = cms.EDFilter("DTNoiseComputation",
    debug = cms.untracked.bool(False),
    fastAnalysis = cms.untracked.bool(False),
    #Total number of events	
    MaxEvents = cms.untracked.int32(300000),
    rootFileName = cms.untracked.string('DTNoiseCalib.root'),
    #Name of the ROOT file which will contains the
    newRootFileName = cms.untracked.string('DTNoiseComp.root')
)

process.p = cms.Path(process.dtunpacker*process.noiseCalib)


