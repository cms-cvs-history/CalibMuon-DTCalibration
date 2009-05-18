#!/bin/tcsh

if ($#argv != 1) then
    echo "************** Argument Error: 1 arg. required **************"
    echo "   Usage:"
    echo "     ./dtTtrigValidChain.csh <run number>"
    echo "*************************************************************"
    exit 1
endif

set runn=$1

set runp=`tail +5 DBTags.dat | grep runperiod | awk '{print $2}'`
set cmsswarea=`tail +5 DBTags.dat | grep cmsswwa | awk '{print $2}'`
set conddbversion=`tail +5 DBTags.dat | grep conddbvs | awk '{print $2}'`
set datasetpath=`tail +5 DBTags.dat | grep dataset | awk '{print $2}'`
set mapdb=`tail +5 DBTags.dat | grep map | awk '{print $2}'`
set t0db=`tail +5 DBTags.dat | grep t0 | awk '{print $2}'`
set noisedb=`tail +5 DBTags.dat | grep noise | awk '{print $2}'`
set muondigi=`tail +5 DBTags.dat | grep dtDigi | awk '{print $2}'`
set vdriftdb=`tail +5 DBTags.dat | grep vdrift | awk '{print $2}'`
set refttrigdb=`tail +5 DBTags.dat | grep refttrig | awk '{print $2}'`

setenv workDir `pwd`
setenv cmsswDir "${HOME}/$cmsswarea"

source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh

cd $cmsswDir
eval `scramv1 runtime -csh`

    cd ${workDir}/Run${runn}/Ttrig/Validation

    foreach lastCrab (crab_0_*)
	set crabDir=$lastCrab
    end

    if( ! ( -e ${crabDir}/res/DTkFactValidation_${runn}.root ) ) then
	source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
	crab -getoutput
    endif

    cd ${crabDir}/res
    if( ! -e ./DQM_1.root ) then
	echo "WARNING: no DQM_xxx.root file found! Exiting!"
	exit 1
    endif

cd ${cmsswDir}/DQM/DTMonitorModule/test

cp DTkFactValidation_2_DQM_TEMPL_cfg.py ${workDir}/Run${runn}/Ttrig/Validation/${crabDir}/res

cd ${workDir}/Run${runn}/Ttrig/Validation/${crabDir}/res

setenv SourceDir ${workDir}'/Run'${runn}'/Ttrig/Validation/'${crabDir}'/res'

echo "${crabDir}/res"
echo "${SourceDir}"
cat >! DTkFactValidation_2_DQM_TEMPL_cfg.py <<EOF
import FWCore.ParameterSet.Config as cms

process = cms.Process("EDMtoMEConvert")
process.load("DQMServices.Components.EDMtoMEConverter_cff")
process.options = cms.untracked.PSet(
 fileMode = cms.untracked.string('FULLMERGE')
)


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Geometry.DTGeometry.dtGeometry_cfi")
process.DTGeometryESModule.applyAlignment = False
process.load("Geometry.MuonNumbering.muonNumberingInitialization_cfi")
process.load("CondCore.DBCommon.CondDBSetup_cfi")
process.load("DQMServices.Core.DQM_cfg")
process.load("RecoLocalMuon.Configuration.RecoLocalMuonCosmics_cff")


process.source = cms.Source("PoolSource",
    processingMode = cms.untracked.string("RunsLumisAndEvents"),
    fileNames = cms.untracked.vstring(
EOF

set CafPath="\t'file:${SourceDir}"
echo "${CafPath}"

foreach TmpFile (`ls ${SourceDir} | grep DQM | grep root`)

    set LastFile=$TmpFile
end

foreach SourceFile (`ls ${SourceDir} | grep DQM | grep root`)
    if ($SourceFile != $LastFile) then
	echo ${CafPath}"/${SourceFile}'," >>  DTkFactValidation_2_DQM_TEMPL_cfg.py
    else
	echo ${CafPath}"/${SourceFile}'" >>  DTkFactValidation_2_DQM_TEMPL_cfg.py
    endif 
end

cat >> DTkFactValidation_2_DQM_TEMPL_cfg.py <<EOF


    )
)


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)
process.eventInfoProvider = cms.EDFilter("EventCoordinatesSource",
    eventInfoFolder = cms.untracked.string('EventInfo/')
)

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('resolutionTest_step1', 
        'resolutionTest_step2', 
        'resolutionTest_step3'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('ERROR'),
        default = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        FwkJob = cms.untracked.PSet(
            limit = cms.untracked.int32(0)
        ),
        resolution = cms.untracked.PSet(
            limit = cms.untracked.int32(10000000)
        ),
        noLineBreaks = cms.untracked.bool(True)
    ),
    categories = cms.untracked.vstring('resolution'),
    destinations = cms.untracked.vstring('cout')
)

process.qTester = cms.EDFilter("QualityTester",
    prescaleFactor = cms.untracked.int32(1),
    qtList = cms.untracked.FileInPath('DQM/DTMonitorClient/test/QualityTests_ttrig.xml')
)

process.load("DQM.DTMonitorClient.dtResolutionTest_cfi")
process.modulo1=process.resolutionTest.clone()
process.modulo1.histoTag2D = 'hResDistVsDist_STEP1' 
process.modulo1.histoTag  = 'hResDist_STEP1'
process.modulo1.STEP = 'STEP1'

process.load("DQM.DTMonitorClient.dtResolutionTest_cfi")
process.modulo2=process.resolutionTest.clone()
process.modulo2.histoTag2D = 'hResDistVsDist_STEP2' 
process.modulo2.histoTag  = 'hResDist_STEP2'
process.modulo2.STEP = 'STEP2'

process.load("DQM.DTMonitorClient.dtResolutionTest_cfi")
process.modulo3=process.resolutionTest.clone()
process.modulo3.histoTag2D = 'hResDistVsDist_STEP3' 
process.modulo3.histoTag  = 'hResDist_STEP3'
process.modulo3.STEP = 'STEP3'



process.source.processingMode = "RunsAndLumis"
process.DQMStore.referenceFileName = ''
process.dqmSaver.convention = 'Offline'
process.dqmSaver.workflow = '/Muon/Dt/Test1'
process.DQMStore.collateHistograms = False
process.EDMtoMEConverter.convertOnEndLumi = True
process.EDMtoMEConverter.convertOnEndRun = False

process.p = cms.Path(process.EDMtoMEConverter*process.modulo1*process.modulo2*process.modulo3*process.qTester*process.dqmSaver)
process.DQM.collectorHost = ''

EOF

cp DTkFactValidation_2_DQM_TEMPL_cfg.py  ${cmsswDir}/DQM/DTMonitorModule/test
cd ${cmsswDir}/DQM/DTMonitorModule/test

cat  DTkFactValidation_2_DQM_TEMPL_cfg.py | sed "s?RUNNUMBERTEMPLATE?${runn}?g"   | sed "s?RUNPERIODTEMPLATE?${runp}?g" >! DTkFactValidation_2_DQM_${runn}_cfg.py


echo "Starting cmsRun DTkFactValidation_2_DQM_${runn}.cfg"
cmsRun DTkFactValidation_2_DQM_${runn}_cfg.py >&! DQMResiduals_${runn}.log

cp DQM_V*.root /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/


echo "Finished cmsRun DTkFactValidation_2_DQM_${runn}.cfg"
cd $workDir
echo "DT DQM validation chain completed successfully!"


echo "DT DQMOffline validation started"
cd ${cmsswDir}/DQMOffline/CalibMuon/test
cat DTtTrigDBValidation_ORCONsqlite_TEMP_cfg.py | sed "s?REFTTRIGTEMPLATE?${refttrigdb}?g" | sed "s?CMSCONDVSTEMPLATE?${conddbversion}?g"| sed "s?RUNNUMBERTEMPLATE?${runn}?g"   | sed "s?RUNPERIODTEMPLATE?${runp}?g" >!  DTtTrigDBValidation_ORCONsqlite_${runn}_cfg.py
cmsRun DTtTrigDBValidation_ORCONsqlite_${runn}_cfg.py >&! DTtTrigDBValidation_${runn}.log

cp tTrigDBMonitoring_${runn}.root /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/


echo "DT DQMOffline validation completed successfully!"



exit 0
