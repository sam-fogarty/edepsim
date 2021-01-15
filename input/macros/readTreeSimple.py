#! /usr/bin/env python
#
# Read almost every field in the event tree.
#

from __future__ import print_function
import glob, os, re, sys, getopt
import ROOT
from ROOT import TCanvas, TPad, TFormula, TF1, TPaveLabel, TH1F, TFile
from ROOT import *
#from ROOT import gSystem
gSystem.Load("libedepsim_io.so")
from ROOT import TG4Event
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Print the fields in a TG4PrimaryParticle object
def printPrimaryParticle(depth, primaryParticle,energies):
    print(depth,"Class: ", primaryParticle.ClassName())
    #print(depth,"Track Id:", primaryParticle.GetTrackId())
    print(depth,"Name:", primaryParticle.GetName())
    #print(depth,"PDG Code:",primaryParticle.GetPDGCode())
    print(depth,"Momentum:",primaryParticle.GetMomentum().X(),
          primaryParticle.GetMomentum().Y(),
          primaryParticle.GetMomentum().Z(),
          primaryParticle.GetMomentum().E(),
          primaryParticle.GetMomentum().P(),
          primaryParticle.GetMomentum().M())
    energies.append(primaryParticle.GetMomentum().E())

# Print the fields in an TG4PrimaryVertex object
def printPrimaryVertex(depth, primaryVertex,energies):
    print(depth,"Class: ", primaryVertex.ClassName())
    print(depth,"Position:", primaryVertex.GetPosition().X(),
          primaryVertex.GetPosition().Y(),
          primaryVertex.GetPosition().Z(),
          primaryVertex.GetPosition().T())
    #print(depth,"Generator:",primaryVertex.GetGeneratorName())
    #print(depth,"Reaction:",primaryVertex.GetReaction())
    #print(depth,"Filename:",primaryVertex.GetFilename())
    print(depth,"InteractionNumber:",primaryVertex.GetInteractionNumber())
    depth = depth + ".."
    for infoVertex in primaryVertex.Informational:
        printPrimaryVertex(depth,infoVertex)
    for primaryParticle in primaryVertex.Particles:
        printPrimaryParticle(depth,primaryParticle,energies)

# Print the fields in a TG4TrajectoryPoint object
def printTrajectoryPoint(depth, trajectoryPoint):
    print(depth,"Class: ", trajectoryPoint.ClassName())
    print(depth,"Position:", trajectoryPoint.GetPosition().X(),
          trajectoryPoint.GetPosition().Y(),
          trajectoryPoint.GetPosition().Z(),
          trajectoryPoint.GetPosition().T())
    print(depth,"Momentum:", trajectoryPoint.GetMomentum().X(),
          trajectoryPoint.GetMomentum().Y(),
          trajectoryPoint.GetMomentum().Z(),
          trajectoryPoint.GetMomentum().Mag())
    print(depth,"Process",trajectoryPoint.GetProcess())
    print(depth,"Subprocess",trajectoryPoint.GetSubprocess())

# Print the fields in a TG4Trajectory object
def printTrajectory(depth, trajectory):
    print(depth,"Class: ", trajectory.ClassName())
    depth = depth + ".."
    print(depth,"Track Id/Parent Id:",
          trajectory.GetTrackId(),
          trajectory.GetParentId())
    print(depth,"Name:",trajectory.GetName())
    print(depth,"PDG Code",trajectory.GetPDGCode())
    print(depth,"Initial Momentum:",trajectory.GetInitialMomentum().X(),
          trajectory.GetInitialMomentum().Y(),
          trajectory.GetInitialMomentum().Z(),
          trajectory.GetInitialMomentum().E(),
          trajectory.GetInitialMomentum().P(),
          trajectory.GetInitialMomentum().M())
    for trajectoryPoint in trajectory.Points:
        printTrajectoryPoint(depth,trajectoryPoint)

# Print the fields in a TG4HitSegment object
def printHitSegment(depth, hitSegment,energyDep_h,xpos,ypos,zpos,x_start,x_end,y_start,y_end,z_start,z_end,totalEDep):
    print(depth,"Class: ", hitSegment.ClassName())
    print(depth,"Primary Id:", hitSegment.GetPrimaryId());
    print(depth,"Energy Deposit:",hitSegment.GetEnergyDeposit())
    energyDep_h.Fill(hitSegment.GetEnergyDeposit())
    print(depth,"Secondary Deposit:", hitSegment.GetSecondaryDeposit())
    print(depth,"Track Length:",hitSegment.GetTrackLength())
    print(depth,"Start:", hitSegment.GetStart().X(),
          hitSegment.GetStart().Y(),
          hitSegment.GetStart().Z(),
          hitSegment.GetStart().T())
    print(depth,"Stop:", hitSegment.GetStop().X(),
          hitSegment.GetStop().Y(),
          hitSegment.GetStop().Z(),
          hitSegment.GetStop().T())
    
    energyDepSegment = hitSegment.GetEnergyDeposit()
    print("Energy Deposit: ", energyDepSegment)
    #totalEDep = totalEDep + energyDepSegment
    
    xpos.append(hitSegment.GetStart().X())
    xpos.append(hitSegment.GetStop().X())
    ypos.append(hitSegment.GetStart().Y())
    ypos.append(hitSegment.GetStop().Y())
    zpos.append(hitSegment.GetStart().Z())
    zpos.append(hitSegment.GetStop().Z())

    x_start.append(hitSegment.GetStart().X())
    x_end.append(hitSegment.GetStop().X())
    y_start.append(hitSegment.GetStart().Y())
    y_end.append(hitSegment.GetStop().Y())
    z_start.append(hitSegment.GetStart().Z())
    z_end.append(hitSegment.GetStop().Z())
    
    
    #print(depth,"Contributor:", [contributor for contributor in hitSegment.Contrib])
    return energyDepSegment

def plotTracks(xpos,ypos,zpos,ax1):
    xpos,ypos,zpos = np.array(xpos)/10.,np.array(ypos)/10.,np.array(zpos)/10.
    #fig1, axes1 = plt.subplots(nrows=1, ncols=1, sharex=True, sharey=True, figsize=(20,8))
    #ax1 = axes1
    
    i = 0
    while i <= (np.size(xpos)/2):
        xstartstop = np.array([xpos[i], xpos[i+1]])
        ystartstop = np.array([ypos[i], ypos[i+1]])
        zstartstop = np.array([zpos[i], zpos[i+1]])

        ax1.plot(xstartstop,ystartstop,zstartstop,linewidth = 2)
        i = i + 2

def plotEvsEDep(energyDeps,energies,muonrestenergy,ax2):
    print("energy deposited: ",energyDeps)
    print("particle energy: ",energies)
    energies = np.array(energies)
    ax2.plot(energies - muonrestenergy,energyDeps,'bo',linewidth = 2)
    ax2.set_title("Total energy deposited vs kinetic energy of particle",fontsize = 15)
    ax2.set_xlabel("Energy of Particle (MeV)",fontsize = 15)
    ax2.set_ylabel("Total energy deposited by particle",fontsize = 15)

# Print the fields in a single element of the SegmentDetectors map.
# The container name is the key, and the hitSegments is the value (a
# vector of TG4HitSegment objects).
def printSegmentContainer(depth, containerName, hitSegments, energyDep_h,dEdx_h,xpos,ypos,zpos,x_start,x_end,y_start,y_end,z_start,z_end,ax1,energyDeps):
    print(depth,"Detector: ", containerName, hitSegments.size())
    depth = depth + ".."
    Eseg = 0
    totalEDep = 0
    dE = []
    for hitSegment in hitSegments: 
        Eseg = printHitSegment(depth, hitSegment,energyDep_h,xpos,ypos,zpos,x_start,x_end,y_start,y_end,z_start,z_end,totalEDep)
        totalEDep = totalEDep + Eseg
        dE.append(Eseg)

    energyDeps.append(totalEDep)
    x_start,x_end,y_start,y_end,z_start,z_end = np.array(x_start),np.array(x_end),np.array(y_start),np.array(y_end),np.array(z_start),np.array(z_end)
    dx = np.sqrt(pow(x_end-x_start, 2) + pow(y_end-y_start, 2) + pow(z_end-z_start, 2)) / 10. # to get cm from mm
    dE = np.array(dE)
    dEdx = dE/dx
    for i in range(np.size(dEdx)): dEdx_h.Fill(dEdx[i])
    plotTracks(xpos,ypos,zpos,ax1)

# Read a file and dump it.
def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    muonrestenergy = 105.65838
# The input file is generated in a previous test (100TestTree.sh).
#inputFile=TFile("SingleCube_edepsim.root")
    inputFile=TFile("test2.root")

    # Get the input tree out of the file.
    inputTree=inputFile.Get("EDepSimEvents")
    print("Class:",inputTree.ClassName())

    # Attach a brach to the events.
    event = TG4Event()
    inputTree.SetBranchAddress("Event",event)

    # Read all of the events.
    entries=inputTree.GetEntriesFast()
    
    # create histogram for energy deposition per segment
    energyDep_h = ROOT.TH1F("Energy Deposition per Segment", "energy deposition",70, 0.0,1.5)
    dEdx_h = ROOT.TH1F("dEdx (MeV/cm)", "dE/dx (MeV/cm)",30,0.0, 5.0)
    
    # create plot for visualizing the tracks (by plotting segments)
    """
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_title("Energy Dep. Tracks for Each Particle", fontsize = 15)
    ax1.set_xlabel("x position")
    ax1.set_ylabel("y position")
    ax1.set_zlabel("z position")
    """
    energies = [] # fill with each particle's energy
    energyDeps = [] # fill with total energy deposited per particle
    for jentry in xrange(entries):
        nb = inputTree.GetEntry(jentry)
        if nb<=0: continue
        print("Class: ", event.ClassName())
        print("Event number:", event.EventId)
        # Dump the primary vertices
        
        for primaryVertex in event.Primaries:
            printPrimaryVertex("PP", primaryVertex,energies)
            # Dump the trajectories
            #for trajectory in event.Trajectories: printTrajectory("TT",trajectory)
            # Dump the segment containers
            print("Number of segment containers:", event.SegmentDetectors.size())
        xpos, ypos, zpos = [],[],[]
        x_start,x_end,y_start,y_end,z_start,z_end = [],[],[],[],[],[]
        for containerName, hitSegments in event.SegmentDetectors:
            printSegmentContainer("HH", containerName, hitSegments,energyDep_h,dEdx_h,xpos,ypos,zpos,x_start,x_end,y_start,y_end,z_start,z_end,ax1,energyDeps)
    
    # create plot for energy vs energy deposited
    #fig2, ax2 = plt.subplots(nrows=1, ncols=1,figsize=(20,8))
    #plotEvsEDep(energyDeps,energies,muonrestenergy,ax2)

    EDepCanvas = ROOT.TCanvas("EDepCanvas","EDep",640,480)

    energyDep_h.GetXaxis().SetTitle("Energy Deposition Per Track")
    energyDep_h.GetYaxis().SetTitle("Frequency")
    

    dEdxCanvas = ROOT.TCanvas("dEdxCanvas","dEdx",640,480)
    dEdx_h.GetXaxis().SetTitle("dE/dx (MeV/cm)")
    dEdx_h.GetYaxis().SetTitle("Frequency")
    #dEdx_h.Draw()

    #hfile = TFile("/dune/data/users/sfogarty/edep-sim/output/edepsimHistos.root","RECREATE","ROOT file for histograms made with edep-sim")
    #energyDep_h.Write()
    #hfile.Close()
    #plt.show()
    energyDep_h.Draw()
    val = 0
    while (val != 1):
        val = input("Enter 1 to end program: ")
if __name__ == "__main__":
    sys.exit(main())
