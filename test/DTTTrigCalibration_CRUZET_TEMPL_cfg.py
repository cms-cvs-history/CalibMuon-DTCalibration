# The following comments couldn't be translated into the new config version:

#Service to write DB if ttrigcalib.findTMeanAndSigma is true

import FWCore.ParameterSet.Config as cms

process = cms.Process("TTRIGCALIBPROC")
process.load("Geometry.MuonCommonData.muonIdealGeometryXML_cfi")

process.load("Geometry.DTGeometry.dtGeometry_cfi")

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.source = cms.Source("PoolSource",
    useCSA08Kludge = cms.untracked.bool(True),
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
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
        tag = cms.string('map_CRUZET')
    ), 
        cms.PSet(
            record = cms.string('DTT0Rcd'),
            tag = cms.string('TZEROTEMPLATE')
        ), 
        cms.PSet(
            record = cms.string('DTStatusFlagRcd'),
            tag = cms.string('NOISETEMPLATE')
        )),
    connect = cms.string('oracle://cms_orcoff_prod/CMS_COND_20X_DT'),
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

process.ttrigcalib = cms.EDFilter("DTTTrigCalibration",
    # Switch on/off the check of noisy channels
    checkNoisyChannels = cms.untracked.bool(True),
    # Module for t0 subtraction
    tTrigMode = cms.untracked.string('DTTTrigSyncT0Only'),
    # Switch on/off the subtraction of t0 from pulses
    doSubtractT0 = cms.untracked.bool(True),
    # Max number of digi per layer to reject a chamber
    maxDigiPerLayer = cms.untracked.int32(10),
    # Label to retrieve DT digis from the event
    digiLabel = cms.untracked.string('dtunpacker'),
    # Name of the ROOT file which will contain the time boxes
    rootFileName = cms.untracked.string('DTTimeBoxes.root'),
    # Switch on/off the DB writing
    fitAndWrite = cms.untracked.bool(True),
    debug = cms.untracked.bool(False),
    # Parameter set for t0 subtraction module
    tTrigModeConfig = cms.untracked.PSet(
        debug = cms.untracked.bool(False)
    ),
    # Tbox rising edge fit parameter
    sigmaTTrigFit = cms.untracked.double(5.0)
)

process.p = cms.Path(process.dtunpacker*process.ttrigcalib)


