#ifndef DTTTrigWriter_H
#define DTTTrigWriter_H

/* Program to evaluate ttrig and sigma ttrig from TB histograms
 *  and write the results to a file for each SL
 
 *  $Date: 2006/09/07 15:30:25 $
 *  $Revision: 1.0 $
 *  \author S. Bolognesi
 */

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/MuonDetId/interface/DTSuperLayerId.h"

#include <string>

namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TFile;
class DTTimeBoxFitter;
class DTTtrig;

class DTTTrigWriter : public edm::EDAnalyzer {
public:
  /// Constructor
  DTTTrigWriter(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~DTTTrigWriter();

  // Operations

  // Compute the ttrig by fiting the TB rising edge
  void analyze(const edm::Event & event, const edm::EventSetup& eventSetup);

  //Write ttrig in the DB
  void endJob();

 
protected:

private:
  // Generate the time box name
  std::string getTBoxName(const DTSuperLayerId& slId) const;

  // Debug flag
  bool debug;

  // The file which contains the tMax histograms
  TFile *theFile;

  // The name of the input root file which contains the tMax histograms
  std::string theRootInputFile;

  // The fitter
  DTTimeBoxFitter *theFitter;

 // The object to be written to DB
  DTTtrig* tTrig; 

};
#endif
