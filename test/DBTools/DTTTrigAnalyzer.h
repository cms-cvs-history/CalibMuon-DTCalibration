#ifndef DTTTrigAnalyzer_H
#define DTTTrigAnalyzer_H

/** \class DTTTrigAnalyzer
 *  Plot the ttrig from the DB
 *
 *  $Date: 2007/03/28 17:19:28 $
 *  $Revision: 1.1 $
 *  \author S. Bolognesi - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/MuonDetId/interface/DTWireId.h"

#include <string>
#include <fstream>
#include <vector>

class DTTtrig;
class TFile;
class TH1D;

class DTTTrigAnalyzer : public edm::EDAnalyzer {
public:
  /// Constructor
  DTTTrigAnalyzer(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~DTTTrigAnalyzer();

  /// Operations
  //Read the DTGeometry and teh t0 DB
  void beginJob(const edm::EventSetup& setup);
  void analyze(const edm::Event& event, const edm::EventSetup& setup) {}
  //Do the real work
  void endJob();

protected:

private:
  std::string getHistoName(const DTWireId& lId) const;
  std::string getDistribName(const DTWireId& wId) const;

  // The file which will contain the histos
  TFile *theFile;

  //The t0 map
  const DTTtrig *tTrigMap;
 
  //The k factor
  double kfactor;
  
  // Map of the ttrig, tmean, sigma histos by wheel/sector/SL
  std::map<std::pair<int,int>, TH1D*> theTTrigHistoMap;
  std::map<std::pair<int,int>, TH1D*> theTMeanHistoMap;
  std::map<std::pair<int,int>, TH1D*> theSigmaHistoMap;
 // Map of the ttrig, tmean, sigma distributions by wheel/station/SL
  std::map<std::vector<int>, TH1D*> theTTrigDistribMap;
  std::map<std::vector<int>, TH1D*> theTMeanDistribMap;
  std::map<std::vector<int>, TH1D*> theSigmaDistribMap;

};
#endif
