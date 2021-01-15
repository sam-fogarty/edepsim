#include "G4RunManager.hh"
#include "G4UImanager.hh"
#include "G4UIExecutive.hh"
#include "ExG4DetectorConstruction01.hh"
#include "ExG4PhysicsList00.hh"
#include "ExG4PrimaryGeneratorAction01.hh"
int main()
{
// construct the default run manager
G4RunManager* runManager = new G4RunManager;
// set mandatory initialization classes
//runManager->SetUserInitialization(new ExG4DetectorConstruction01);
//runManager->SetUserInitialization(new ExG4PhysicsList00);

// set mandatory user action class
//runManager->SetUserAction(new ExG4PrimaryGeneratorAction01);
// initialize G4 kernel
//runManager->Initialize();
// Get the pointer to the User Interface manager
//G4UImanager* UImanager = G4UImanager::GetUIpointer();
//if ( argc == 1 ) {
// interactive mode : define UI session
//G4UIExecutive* ui = new G4UIExecutive(argc, argv);
//UImanager->ApplyCommand("/control/execute init.mac");
//ui->SessionStart();
//delete ui;
//}
//else {
// batch mode
//G4String command = "/control/execute ";
//G4String fileName = argv[1];
//UImanager->ApplyCommand(command+fileName);
//}
// job termination
delete runManager;
return 0;
}
