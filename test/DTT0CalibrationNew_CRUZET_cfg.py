import FWCore.ParameterSet.Config as cms

process = cms.Process("MONITOR")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Geometry.MuonCommonData.muonIdealGeometryXML_cfi")

process.load("Geometry.DTGeometry.dtGeometry_cfi")

process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")

process.source = cms.Source("PoolSource",
    useCSA08Kludge = cms.untracked.bool(True),
    debugFlag = cms.untracked.bool(True),
    debugVebosity = cms.untracked.uint32(10),
    fileNames = cms.untracked.vstring('/store/data/CRUZET3/Cosmics/RAW/v1/000/051/125/088EC52F-834E-DD11-AB71-001617C3B5F4.root', 
        '/store/data/CRUZET3/Cosmics/RAW/v1/000/051/125/0E7FD0EF-7F4E-DD11-B50E-001617C3B706.root', 
        '/store/data/CRUZET3/Cosmics/RAW/v1/000/051/125/26BFC1D4-7E4E-DD11-91F7-001617E30E28.root', 
        '/store/data/CRUZET3/Cosmics/RAW/v1/000/051/125/2A7A17C0-794E-DD11-9B96-000423D9863C.root', 
        '/store/data/CRUZET3/Cosmics/RAW/v1/000/051/125/30A5D457-804E-DD11-B416-000423D985E4.root')
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100000)
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
    process.CondDBSetup,
    timetype = cms.string('runnumber'),
    toGet = cms.VPSet(cms.PSet(
        record = cms.string('DTReadOutMappingRcd'),
        tag = cms.string('map_CRUZET')
    ), 
        cms.PSet(
            record = cms.string('DTTtrigRcd'),
            tag = cms.string('tTrig_CRUZET_080708_2019')
        )),
    connect = cms.string('frontier://FrontierProd/CMS_COND_20X_DT')
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(
        authenticationPath = cms.untracked.string('/afs/cern.ch/cms/DB/conddb')
    ),
    authenticationMethod = cms.untracked.uint32(0),
    connect = cms.string('sqlite_file:t0.db'),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTT0Rcd'),
        tag = cms.string('t0')
    ))
)

process.t0calib = cms.EDFilter("DTT0CalibrationNew",
    # Cells for which you want the histos (default = None)
    cellsWithHisto = cms.untracked.vstring('-1 8 1 1 3 48', 
        '-1 8 1 1 3 49', 
        '-1 8 1 1 2 49', 
        '-1 8 1 1 2 50', 
        '-1 8 1 1 1 48', 
        '-1 8 1 1 1 49'),
    # Criteria to reject digis away from TP peak
    rejectDigiFromPeak = cms.uint32(50),
    # Label to retrieve DT digis from the event
    digiLabel = cms.untracked.string('dtunpacker'),
    calibSector = cms.untracked.string('All'),
    # Chose the wheel, sector (default = All)
    calibWheel = cms.untracked.string('All'),
    # Number of events to be used for the t0 per layer histos
    eventsForWireT0 = cms.uint32(5000),
    # Name of the ROOT file which will contain the test pulse times per layer
    rootFileName = cms.untracked.string('DTTestPulses.root'),
    debug = cms.untracked.bool(True),
    # Acceptance for TP peak width
    tpPeakWidth = cms.double(5.0),
    # Time box width (TP within time box)
    timeBoxWidth = cms.uint32(500),
    # Number of events to be used for the t0 per layer histos
    eventsForLayerT0 = cms.uint32(3000)
)

process.p = cms.Path(process.dtunpacker*process.t0calib)


