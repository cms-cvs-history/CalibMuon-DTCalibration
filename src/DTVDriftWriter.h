#ifndef DTVDriftWriter_H
#define DTVDriftWriter_H

/* Program to evaluate v_drift and t0 from TMax histograms
 *  and write the results to a file for each SL
 
 *  $Date: 2006/08/31 15:30:25 $
 *  $Revision: 1.1 $
 *  \author M. Giunta - e-mail:marina.giunta@cern.ch
 */


#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/MuonDetId/interface/DTWireId.h"

#include <string>
#include <vector> 


namespace edm {
  class ParameterSet;
  class Event;
  class EventSetup;
}

class TFile;
class DTMtime;

class DTVDriftWriter : public edm::EDAnalyzer {
public:
  /// Constructor
  DTVDriftWriter(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~DTVDriftWriter();

  // Operations
  void endJob();

  void analyze(const edm::Event & event, const edm::EventSetup& eventSetup);
 
  std::vector<float> evaluateVDriftAndReso (const DTWireId& wireId);
protected:

private:
  // Debug flag
  bool debug;

  // The file which contains the tMax histograms
  TFile *theFile;

  // The name of the input root file which contains the tMax histograms
  std::string theRootInputFile;

  // The name of the output text file
  std::string theVDriftOutputFile;

  //parameter set for DTCalibrationMap constructor
  edm::ParameterSet theCalibFilePar;
  
  // the granularity to be used for calib consts evaluation
  std::string theGranularity;

  // The object to be written to DB
  DTMtime* theMTime;

};
#endif