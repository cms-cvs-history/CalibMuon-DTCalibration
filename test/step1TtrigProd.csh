#!/bin/tcsh

if ($#argv != 1) then
    echo "************** Argument Error: 1 arg. required **************"
    echo "   Usage:"
    echo "     ./submitTtrigProd.csh <run number>"
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

if( ! -d ./Run`echo $runn` ) then
    mkdir Run`echo $runn`
endif

if( ! -d ./Run`echo $runn`/Ttrig ) then
    mkdir Run`echo $runn`/Ttrig
endif

if( ! -d ./Run`echo $runn`/Ttrig/Production ) then
    mkdir Run`echo $runn`/Ttrig/Production
endif

source /afs/cern.ch/cms/LCG/LCG-2/UI/cms_ui_env.csh

cd $cmsswDir
eval `scramv1 runtime -csh`

cd CalibMuon/DTCalibration/test
cat crab_ttrig_prod_TEMPL.cfg | sed "s?DATASETPATHTEMPLATE?${datasetpath}?g" | sed "s/RUNNUMBERTEMPLATE/${runn}/g" >! ${workDir}/Run${runn}/Ttrig/Production/crab.cfg
#cat DTTTrigCalibration_TEMPL_cfg.py | sed "s/DIGITEMPLATE/${muondigi}/g" | sed "s/MAPTEMPLATE/${mapdb}/g"| sed "s/TZEROTEMPLATE/${t0db}/g" | sed "s/NOISETEMPLATE/${noisedb}/g" | sed "s?CMSCONDVSTEMPLATE?${conddbversion}?g" >! ${workDir}/Run${runn}/Ttrig/Production/DTTTrigCalibration_cfg.py
cat DTTTrigCalibration_TEMPL_cfg.py | sed "s/DIGITEMPLATE/${muondigi}/g" | sed "s/GLOBALTAGTEMPLATE/${globaltag}/g" >! ${workDir}/Run${runn}/Ttrig/Production/DTTTrigCalibration_cfg.py

cd ${workDir}/Run${runn}/Ttrig/Production

source /afs/cern.ch/cms/ccs/wm/scripts/Crab/crab.csh
#source /afs/cern.ch/cms/ccs/wm/scripts/Crab/CRAB_2_5_1/crab.csh

crab -create -submit all
cd ${workDir}

exit 0
