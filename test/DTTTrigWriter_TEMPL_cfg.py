# The following comments couldn't be translated into the new config version:

#Service to write in the DB

import FWCore.ParameterSet.Config as cms

process = cms.Process("PROD")
process.load("CondCore.DBCommon.CondDBSetup_cfi")

process.load("Configuration.StandardSequences.Geometry_cff")

process.load("FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = "CRAFT_V2P::All"


process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)

process.PoolDBOutputService = cms.Service("PoolDBOutputService",
    DBParameters = cms.PSet(

    ),
    timetype = cms.untracked.string('runnumber'),
    connect = cms.string('sqlite_file:/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/ttrig_first_TEMPLATE.db'),
    authenticationMethod = cms.untracked.uint32(0),
    toPut = cms.VPSet(cms.PSet(
        record = cms.string('DTTtrigRcd'),
        tag = cms.string('ttrig')
    ))
)


process.load("CalibMuon.DTCalibration.DTTTrigWriter_cfi.py")
process.ttrigwriter.kFactor = -0.7
process.ttrigwriter.rootFileName = "/afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/CRUZET/ttrig/DTTimeBoxes_TEMPLATE.root"


process.p = cms.Path(process.ttrigwriter)


