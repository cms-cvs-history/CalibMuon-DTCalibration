#ifndef ToChamberRefT0DB_H
#define ToChamberRefT0DB_H

/** \class ToChamberRefT0DB
 *  Class which read a t0 DB and modifies it passing
 *  to a reference offset by chamber
 *
 *  $Date: 2007/11/09 17:55:38 $
 *  $Revision: 1.1 $
 *  \author S. Bolognesi - INFN Torino
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include <FWCore/Framework/interface/ESHandle.h>

#include <string>

class DTT0;

class ToChamberRefT0DB : public edm::EDAnalyzer {
public:
  /// Constructor
  ToChamberRefT0DB(const edm::ParameterSet& pset);

  /// Destructor
  virtual ~ToChamberRefT0DB();

  // Operations

  virtual void beginJob(const edm::EventSetup& setup);

  virtual void analyze(const edm::Event& event, const edm::EventSetup& setup){}

  virtual void endJob();

protected:

private:
  const DTT0 *tZeroMap;
  bool debug;
};
#endif

