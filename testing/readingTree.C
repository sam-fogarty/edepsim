/////////// DOES NOT WORK IN CURRENT FORM, PARTICULARLY THE FOR LOOPS

#include "/dune/data/users/sfogarty/include/TG4Event.h"
#include <iostream>

using namespace std;

void readingTree(){

TFile f("test3.root");
TG4Event *events = NULL;
TTree *tree = (TTree*)f.Get("EDepSimEvents");
tree->SetBranchAddress("Event",&events);
//cout << tree->GetEntries() << endl;
 
 for (auto detector = events->SegmentDetectors.begin(); detector != SegmentDetectors.end(); ++detector)

   {

       for (auto hit = detector.second.begin(); hit != detector.second.end(); ++hit)
         {

	   cout << "Energy Deposit: " << hit->GetEnergyDeposit() << endl;
           cout << "Start X: " << hit->GetStart().X() << endl;
           cout << "Start Y: " << hit->GetStart().Y() << endl;
           cout << "Start Z: " << hit->GetStart().Z() << endl;
           cout << "Length: " << hit->GetTrackLength() << endl;

         }
           cout << " " << endl;

   }




}
