#include <loadEDepSim.h>
#include <TPolyLine3D.h>
#include <TPolyMarker3D.h>
#include <TPad.h>
#include <TColor.h>
#include <TDatabasePDG.h>

#include <TGeoManager.h>


#include "plotEDepSim.h"

#include <iostream>

using namespace std;

void plotEDepSim.C(){



}


int EDepSimPlotTrajectories() {
    TG4Event* event = EDepSimEvent();
    int count = 0;
    for (auto track = event->Trajectories.begin();
         track != event->Trajectories.end();
         ++track) {
        if (!EDepSimPlotTrajectory(track->TrackId)) continue;
        ++count;
    }
    gPad->Update();
    return count;
}

int EDepSimPlotSegmentDetector(std::string name) {
    TG4Event* event = EDepSimEvent();
    for (auto detector = event->SegmentDetectors.begin();
         detector != event->SegmentDetectors.end();
         ++detector) {
        if (detector->first != name) continue;
        std::cout << " Found detector " << name
                  << " with " << detector->second.size() << " Hits"
                  << std::endl;
        if (detector->second.size() < 1) return 0;
        for (auto hit = detector->second.begin();
             hit != detector->second.end();
             ++hit) {
            double length = (hit->Stop.Vect()-hit->Start.Vect()).Mag();
            int iColor = EDepSimLogColor(hit->EnergyDeposit,0.4,2.0);
            if (length > 2.0) {
                TPolyLine3D* line = new TPolyLine3D(2);
                line->SetLineColor(iColor);
                line->SetLineStyle(1);
                line->SetPoint(0,
                               hit->Start.X(),
                               hit->Start.Y(),
                               hit->Start.Z());
                line->SetPoint(1,
                               hit->Stop.X(),
                               hit->Stop.Y(),
                               hit->Stop.Z());
                line->Draw();
                plottedHits.push_back(line);
            }
            else {
                TPolyMarker3D* mark = new TPolyMarker3D(1);
                mark->SetMarkerColor(iColor);
                mark->SetMarkerStyle(kCircle);
                mark->SetMarkerSize(hit->TrackLength/2.0);
                TLorentzVector pos = 0.5*(hit->Start + hit->Stop);
                mark->SetPoint(0, pos.X(), pos.Y(), pos.Z());
                mark->Draw();
                plottedHits.push_back(mark);
            }                
        }
        return detector->second.size();
    }
    return 0;
}
