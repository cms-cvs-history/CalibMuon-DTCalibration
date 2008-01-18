
/*
 *  See header file for a description of this class.
 *
 *  $Date: 2007/11/12 10:32:13 $
 *  $Revision: 1.1 $
 *  \author S. Bolognesi - INFN Torino
 */

#include "ToChamberRefT0DB.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/MuonDetId/interface/DTChamberId.h"

#include "CondFormats/DTObjects/interface/DTT0.h"
#include "CondFormats/DataRecord/interface/DTT0Rcd.h"
#include "CalibMuon/DTCalibration/interface/DTCalibDBUtils.h"

#include <iostream>
#include <fstream>

using namespace edm;
using namespace std;

ToChamberRefT0DB::ToChamberRefT0DB(const ParameterSet& pset) {
  debug = pset.getUntrackedParameter<bool>("debug",false);
}

ToChamberRefT0DB::~ToChamberRefT0DB(){}


void ToChamberRefT0DB::beginJob(const EventSetup& setup) {
   ESHandle<DTT0> t0;
   setup.get<DTT0Rcd>().get(t0);
   tZeroMap = &*t0;
   cout << "[ToChamberRefT0DB]: T0 version: " << t0->version() << endl;
}


void ToChamberRefT0DB::endJob() {
  // Create the object to be written to DB
  DTT0* tZeroNewMap = new DTT0();

  //Compute the reference for each chamber
  map<DTChamberId,double> sumT0ByChamber;
  map<DTChamberId,int> countT0ByChamber;
  for(DTT0::const_iterator tzero = tZeroMap->begin();
      tzero != tZeroMap->end(); tzero++) {
    DTChamberId chamberId((*tzero).first.wheelId,
			  (*tzero).first.stationId,
			  (*tzero).first.sectorId);
    sumT0ByChamber[chamberId] = sumT0ByChamber[chamberId] + (*tzero).second.t0mean;
    countT0ByChamber[chamberId]++;
  }

  //Change reference for each wire and store the new t0s in the new map
  for(DTT0::const_iterator tzero = tZeroMap->begin();
      tzero != tZeroMap->end(); tzero++) {
    DTChamberId chamberId((*tzero).first.wheelId,
			  (*tzero).first.stationId,
			  (*tzero).first.sectorId);
    double t0mean = ((*tzero).second.t0mean) - (sumT0ByChamber[chamberId]/countT0ByChamber[chamberId]);
    double t0rms = (*tzero).second.t0rms;
    DTWireId wireId((*tzero).first.wheelId,
		    (*tzero).first.stationId,
		    (*tzero).first.sectorId,
		    (*tzero).first.slId,
		    (*tzero).first.layerId,
		    (*tzero).first.cellId);
    tZeroNewMap->set(wireId,
		     t0mean,
		     t0rms,
		     DTTimeUnits::counts);
    if(debug){
      //cout<<"Chamber "<<chamberId<<" has reference "<<(sumT0ByChamber[chamberId]/countT0ByChamber[chamberId]);
      cout<<"Changing t0 of wire "<<wireId<<" from "<<(*tzero).second.t0mean<<" to "<<t0mean<<endl;
    }
  }

  //Write object to DB
  cout << "[ToChamberRefT0DB]: Writing t0 object to DB!" << endl;
  string record = "DTT0Rcd";
  DTCalibDBUtils::writeToDB<DTT0>(record, tZeroNewMap);
} 



