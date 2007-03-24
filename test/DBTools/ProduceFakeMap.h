#ifndef ProduceFakeMap_H
#define ProduceFakeMap_H

/** \class ProduceFakeMap
 *  Class which produce fake map of ttrig,t0,vedrift,noise (NO channelsMap)
 *  in a txt file of the same format of CMSSW DTMapCalibration
 *  (see DTCalibrationMap for details)
 *
 *  $Date: 2007/01/24 16:02:14 $
 *  $Revision: 1.0 $
 *  \author S. Bolognesi - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include <FWCore/Framework/interface/ESHandle.h>

#include <string>

class DTCalibrationMap;
class DTGeometry;

class ProduceFakeMap : public edm::EDAnalyzer {
public:
  /// Constructor
  ProduceFakeMap(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~ProduceFakeMap();

  // Operations

  virtual void beginJob(const edm::EventSetup& setup);

  virtual void analyze(const edm::Event& event, const edm::EventSetup& setup){}

  virtual void endJob();

protected:

private:
  edm::ESHandle<DTGeometry> muonGeom;
  DTCalibrationMap *theCalibFile;

  std::string theOutputFileName;

  std::string mapToProduce;

};
#endif

