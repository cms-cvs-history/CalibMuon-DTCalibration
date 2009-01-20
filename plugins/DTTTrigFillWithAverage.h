#ifndef CalibMuon_DTTTrigFillWithAverage_H
#define CalibMuon_DTTTrigFillWithAverage_H

/** \class DTTTrigFillWithAverage
 *  Concrete implementation of a DTTTrigBaseCorrection.
 *  Fills missing tTrig values in DB 
 *
 *  $Revision: 1.2 $
 *  \author A. Vilela Pereira
 */

#include "CalibMuon/DTCalibration/interface/DTTTrigBaseCorrection.h"
#include "FWCore/Framework/interface/ESHandle.h"

namespace edm {
  class ParameterSet;
}

class DTTtrig;
class DTGeometry;

class DTTTrigFillWithAverage: public DTTTrigBaseCorrection {
public:
  // Constructor
  DTTTrigFillWithAverage(const edm::ParameterSet&);

  // Destructor
  virtual ~DTTTrigFillWithAverage();

  virtual void setES(const edm::EventSetup& setup);
  virtual DTTTrigData correction(const DTSuperLayerId&);

private:
  void getAverage();

  const DTTtrig *tTrigMap_;
  edm::ESHandle<DTGeometry> muonGeom_;

  struct {
    double aveMean;
    double rmsMean;
    double aveSigma;
    double rmsSigma;
  } initialTTrig_;

  bool foundAverage_; 
};
#endif