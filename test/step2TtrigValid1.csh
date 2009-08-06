#!/bin/tcsh

if ($#argv != 1) then
    echo "************** Argument Error: 1 arg. required **************"
    echo "   Usage:"
    echo "     ./dtTtrigProdChain.csh <run number>"
    echo "*************************************************************"
    exit 1
endif

set runn=$1

set runp=`tail +5 DBTags.dat | grep runperiod | awk '{print $2}'`
set cmsswarea=`tail +5 DBTags.dat | grep cmsswwa | awk '{print $2}'`
set datasetpath=`tail +5 DBTags.dat | grep dataset | awk '{print $2}'`
set globaltag=`tail +5 DBTags.dat | grep globaltag | awk '{print $2}'`
set muondigi=`tail +5 DBTags.dat | grep dtDigi | awk '{print $2}'`

#set conddbversion=`tail +5 DBTags.dat | grep conddbvs | awk '{print $2}'`
#set mapdb=`tail +5 DBTags.dat | grep map | awk '{print $2}'`
#set t0db=`tail +5 DBTags.dat | grep t0 | awk '{print $2}'`
#set noisedb=`tail +5 DBTags.dat | grep noise | awk '{print $2}'`
#set vdriftdb=`tail +5 DBTags.dat | grep vdrift | awk '{print $2}'`

setenv workDir `pwd`
setenv cmsswDir "${HOME}/$cmsswarea"

unalias ls

cd $cmsswDir
eval `scramv1 runtime -csh`

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/DTTimeBoxes_${runn}.root ) ) then

    cd ${workDir}/Run${runn}/Ttrig/Production

    foreach lastCrab (crab_0_*)
	set crabDir=$lastCrab
    end

    if( ! ( -e ${crabDir}/res/DTTimeBoxes_${runn}.root ) ) then

	source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
	crab -getoutput    # uncomment only if getoutput is needed (leave it commented if getoutput already done!)

	cd ${crabDir}/res

	if( ! -e ./DTTimeBoxes_1.root ) then
	    echo "WARNING: no DTTimeBoxes_xxx.root files found! Exiting!"
	    exit 1
	endif

	hadd DTTimeBoxes_${runn}.root DTTimeBoxes_*.root
	cp DTTimeBoxes_${runn}.root /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/
    endif

endif

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/DTTimeBoxes_${runn}.root ) ) then
    echo "File /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/DTTimeBoxes_${runn}.root not found!"
    echo "Exiting!"
    exit 1
endif

##
## DTTTrigWriter.cfg
##

cd ${cmsswDir}/CalibMuon/DTCalibration/test

#cat DTTTrigWriter_TEMPL_cfg.py | sed "s?RUNPERIODTEMPL?${runp}?g"  | sed "s/TZEROTEMPLATE/${t0db}/g" | sed "s/NOISETEMPLATE/${noisedb}/g"| sed "s?CMSCONDVSTEMPLATE?${conddbversion}?g"| sed "s?TEMPLATE?${runn}?g" >! DTTTrigWriter_${runn}_cfg.py
cat DTTTrigWriter_TEMPL_cfg.py | sed "s?RUNPERIODTEMPL?${runp}?g"  | sed "s/GLOBALTAGTEMPLATE/${globaltag}/g" | sed "s?RUNNUMBERTEMPLATE?${runn}?g" >! DTTTrigWriter_${runn}_cfg.py

echo "Starting cmsRun DTTTrigWriter_${runn}.cfg"
cmsRun DTTTrigWriter_${runn}_cfg.py >&! tmpDTTTrigWriter_${runn}.log
echo "Finished cmsRun DTTTrigWriter_${runn}.cfg"

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/ttrig_first_${runn}.db ) ) then
    echo "DTTTrigWriter_`echo $runn`.cfg did not produce txt file!"
    echo "See tmpDTTTrigWriter_`echo $runn`.log for details"
    echo "(in your CMSSW test directory)."
    exit 1
else
    rm tmpDTTTrigWriter_${runn}.log
    rm DTTTrigWriter_${runn}_cfg.py
endif

set dumpdb="first"

########################################################

##
## DumpDBToFile_first.cfg
##

cat DumpDBToFile_ttrig_TEMPL_cfg.py | sed "s?DUMPDBTEMPL?${dumpdb}?g"  | sed "s?RUNPERIODTEMPL?${runp}?g"  | sed "s?RUNNUMBERTEMPLATE?${runn}?g" >! DumpDBToFile_${dumpdb}_${runn}_cfg.py

echo "Starting cmsRun DumpDBToFile_${dumpdb}_${runn}.cfg"
cmsRun DumpDBToFile_${dumpdb}_${runn}_cfg.py >&! tmpDumpDBToFile_${dumpdb}_${runn}.log
echo "Finished cmsRun DumpDBToFile_${dumpdb}_${runn}.cfg"

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/ttrig_${dumpdb}_${runn}.txt ) ) then
    echo "DumpDBToFile_${dumpdb}_ttrig.cfg did not produce txt file!"
    echo "See tmpDumpDBToFile_${dumpdb}_`echo $runn`.log for details"
    echo "(in your CMSSW test directory)."
    exit 1
else 
    rm tmpDumpDBToFile_${dumpdb}_${runn}.log
    rm DumpDBToFile_${dumpdb}_${runn}_cfg.py
endif

########################################################

##
## DTTTrigCorrection.cfg
##

cat DTTTrigCorrection_TEMPL_cfg.py | sed "s?RUNNUMBERTEMPLATE?${runn}?g" | sed "s?RUNPERIODTEMPL?${runp}?g" >! DTTTrigCorrection_${runn}_cfg.py

echo "Starting cmsRun DTTTrigCorrection_${runn}.cfg"
cmsRun DTTTrigCorrection_${runn}_cfg.py >&! /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/DTTTrigCorrection_${runn}_log.txt
echo "Finished cmsRun DTTTrigCorrection_${runn}.cfg"

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/ttrig_second_${runn}.db ) ) then
    echo "DTTTrigCorrection.cfg did not produce ttrig corrected DataBase!"
    echo "See DTTTrigCorrection_${runn}_log.txt file for details"
    echo "(in /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/)."
    echo "Exiting!"
    exit 1
else
    rm DTTTrigCorrection_${runn}_cfg.py
endif

set dumpdb="second"

########################################################

##
## DumpDBToFile_second.cfg
##

cat DumpDBToFile_ttrig_TEMPL_cfg.py | sed "s?DUMPDBTEMPL?${dumpdb}?g"  | sed "s?RUNPERIODTEMPL?${runp}?g"  | sed "s?RUNNUMBERTEMPLATE?${runn}?g" >! DumpDBToFile_${dumpdb}_${runn}_cfg.py

echo "Starting cmsRun DumpDBToFile_${dumpdb}_${runn}.cfg"
cmsRun DumpDBToFile_${dumpdb}_${runn}_cfg.py >&! tmpDumpDBToFile_${dumpdb}_${runn}.log
echo "Finished cmsRun DumpDBToFile_${dumpdb}_${runn}.cfg"

if( ! ( -e /afs/cern.ch/cms/CAF/CMSALCA/ALCA_MUONCALIB/DTCALIB/${runp}/ttrig/ttrig_${dumpdb}_${runn}.txt ) ) then
    echo "DumpDBToFile_${dumpdb}_ttrig.cfg did not produce txt file!"
    echo "See tmpDumpDBToFile_${dumpdb}_`echo $runn`.log for details"
    echo "(in your CMSSW test directory)."
    exit 1
else 
    rm tmpDumpDBToFile_${dumpdb}_${runn}.log
    rm DumpDBToFile_${dumpdb}_${runn}_cfg.py
endif

cd $workDir

set dumpdb="second"

echo "DT calibration chain completed successfully!"
########################################################

## First Validation on Residuals 
## DTkFactValidation_1_TEMPL_cfg.py
##

if( ! -d ./Run`echo $runn` ) then
    mkdir Run`echo $runn`
endif

if( ! -d ./Run`echo $runn`/Ttrig ) then
    mkdir Run`echo $runn`/Ttrig
endif

if( ! -d ./Run`echo $runn`/Ttrig/Validation ) then
    mkdir Run`echo $runn`/Ttrig/Validation
endif

source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh

cd $cmsswDir
eval `scramv1 runtime -csh`
cd DQM/DTMonitorModule/test
cat crab_Valid_TEMPL.cfg  | sed "s?DUMPDBTEMPL?${dumpdb}?g" | sed "s?DATASETPATHTEMPLATE?${datasetpath}?g" | sed "s/RUNNUMBERTEMPLATE/${runn}/g" | sed "s?RUNPERIODTEMPLATE?${runp}?g" >! ${workDir}/Run${runn}/Ttrig/Validation/crab.cfg
#cat DTkFactValidation_1_TEMPL_cfg.py  | sed "s?DUMPDBTEMPL?${dumpdb}?g" | sed "s/MAPTEMPLATE/${mapdb}/g" | sed "s/VDRIFTTEMPLATE/${vdriftdb}/g"| sed "s/RUNNUMBERTEMPLATE/${runn}/g" | sed "s/TZEROTEMPLATE/${t0db}/g" | sed "s/NOISETEMPLATE/${noisedb}/g" | sed "s?RUNPERIODTEMPLATE?${runp}?g"| sed "s?CMSCONDVSTEMPLATE?${conddbversion}?g" >! ${workDir}/Run${runn}/Ttrig/Validation/DTkFactValidation_1_cfg.py
cat DTkFactValidation_1_TEMPL_cfg.py  | sed "s?DUMPDBTEMPL?${dumpdb}?g" | sed "s/GLOBALTAGTEMPLATE/${globaltag}/g" | sed "s/RUNNUMBERTEMPLATE/${runn}/g" | sed "s?RUNPERIODTEMPLATE?${runp}?g" >! ${workDir}/Run${runn}/Ttrig/Validation/DTkFactValidation_1_cfg.py

cd ${workDir}/Run${runn}/Ttrig/Validation

source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/CRAB_2_5_1/crab.csh

crab -create -submit all
cd ${workDir}

exit 0
