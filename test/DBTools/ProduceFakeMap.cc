
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2007/01/24 16:01:30 $
 *  $Revision: 1.7 $
 *  \author G. Cerminara - INFN Torino
 */

#include "ProduceFakeMap.h"
#include "DTCalibrationMap.h"


#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include "Geometry/Records/interface/MuonGeometryRecord.h"
#include "Geometry/DTGeometry/interface/DTGeometry.h"
#include "Geometry/DTGeometry/interface/DTLayer.h"
#include "Geometry/DTGeometry/interface/DTSuperLayer.h"
#include "Geometry/DTGeometry/interface/DTChamber.h"
#include "Geometry/DTGeometry/interface/DTTopology.h"


#include <iostream>
#include <fstream>

using namespace edm;
using namespace std;

ProduceFakeMap::ProduceFakeMap(const ParameterSet& pset) {
  theCalibFile = new DTCalibrationMap(pset.getUntrackedParameter<ParameterSet>("calibFileConfig"));
  theOutputFileName = pset.getUntrackedParameter<string>("outputFileName");

  mapToProduce = pset.getUntrackedParameter<string>("mapToProduce", "TTrigDB");

  if(mapToProduce != "VDriftDB" && mapToProduce != "TTrigDB" && mapToProduce != "TZeroDB" 
     && mapToProduce != "NoiseDB")
    cout << "[ProduceFakeMap] *** Error: parameter mapToProduce is not valid, check the cfg file" << endl;
}

ProduceFakeMap::~ProduceFakeMap(){}

void ProduceFakeMap::beginJob(const edm::EventSetup& context){
  context.get<MuonGeometryRecord>().get(muonGeom);
}

void ProduceFakeMap::endJob() {
  
  //Get the superlayers and layers list
  vector<DTSuperLayer*> dtSupLylist = muonGeom->superLayers();
  vector<DTLayer*> dtLyList = muonGeom->layers();

  if(mapToProduce == "VDriftDB") {
    //Loop on superlayers
    for (vector<DTSuperLayer*>::const_iterator sl = dtSupLylist.begin();
	 sl != dtSupLylist.end(); sl++) {
      //Define DTWireId
      DTWireId wireId((*sl)->id(), 0, 0);
      vector<float> consts;
      consts.push_back(-1);
      consts.push_back(-1);
      consts.push_back(0.00543); //default vdrift = 0.00543cm/ns
      consts.push_back(0.02); //default hit reoslution = 0.02 cm

      //Add constants to the file
      theCalibFile->addCell(wireId, consts);
    }
  } 
  else if(mapToProduce == "TTrigDB") {
    //Loop on superlayers
    for (vector<DTSuperLayer*>::const_iterator sl = dtSupLylist.begin();
	 sl != dtSupLylist.end(); sl++) {
      //Define DTWireId
      DTWireId wireId((*sl)->id(), 0, 0);
      vector<float> consts;
      consts.push_back(496);
      consts.push_back(0);
      consts.push_back(-1);
      consts.push_back(-1);

      //Add constants to the file
      theCalibFile->addCell(wireId, consts);
    }
  }
  else if(mapToProduce == "TZeroDB") {
    //Loop on layers
    for (vector<DTLayer*>::const_iterator ly = dtLyList.begin();
	 ly != dtLyList.end(); ly++) {
	
      //Get the number of wires for each layer
      int nWires = (*ly)->specificTopology().channels();
      //Loop on wires
      for(int w=1; w<=nWires; w++){
	DTWireId wireId((*ly)->id(), w);
	vector<float> consts;
	consts.push_back(-1);
	consts.push_back(-1);
	consts.push_back(-1);
	consts.push_back(-1);
	consts.push_back(0); //fake ttrig for simulated data      
	consts.push_back(0); //fake sigmattrig for simulated data
	  
	theCalibFile->addCell(wireId, consts);
      }
    }
  }
  else if(mapToProduce == "NoiseDB") {
    //we should have an entry only if the channel is noisy.. producen empty DB for simulated data??
  }
  theCalibFile->writeConsts(theOutputFileName);
}


