This directory is for running edep-sim. Macro files can be found in the "input" directory, output ROOT files (and possibly other output files) in the "output" directory, some testing stuff (reading the edep-sim trees, etc) in the "testing" directory.

The SingleCube geometry (and other geometries I've used or made) can be found (if I haven't changed it) at /dune/data/users/sfogarty/geometry/ .

An example way to run edep-sim is:

   	   edep-sim -C -u -g geometry.gdml -o output.root -e 100 macro.mac

"-C" makes it so it doesn't check for overlaps, "-u" adds /edep/update before first macro is processed, "-g" loads a gdml geometry file, "-o" creates an output file, "-e" sets the number of particles (in the case of single particles) by adding /run/beamOn <n> after last macro is processed, and "-p" sets the physics list.

The macro files contain the GEANT4 code that creates the particle source, particle positions, angles, energies, etc.
