#ifdef __CLING__
R__LOAD_LIBRARY(libDelphes)
#include "classes/DelphesClasses.h"
#include "external/ExRootAnalysis/ExRootTreeReader.h"
#include "external/ExRootAnalysis/ExRootResult.h"
#else
class ExRootTreeReader;
class ExRootResult;
#endif

void ParTpre()
{

    // Using multi-thread if possible
    int nthreads = 6;
    ROOT::EnableImplicitMT(nthreads);
  
    gSystem->Load("libDelphes");

    auto *chain = new TChain("Delphes");
    chain->Add("tag_1_delphes_events.root");

    auto *treeReader = new ExRootTreeReader(chain);
    auto *result = new ExRootResult();

    auto *branchParticle = treeReader->UseBranch("Particle");
    auto *branchElectron = treeReader->UseBranch("Electron");
    auto *branchPhoton = treeReader->UseBranch("Photon");
    auto *branchMuon = treeReader->UseBranch("Muon");
    auto *branchEFlowTrack = treeReader->UseBranch("EFlowTrack");
    auto *branchEFlowPhoton = treeReader->UseBranch("EFlowPhoton");
    auto *branchEFlowNeutralHadron = treeReader->UseBranch("EFlowNeutralHadron");
    auto *branchJet = treeReader->UseBranch("Jet");

    const auto allEntries = treeReader->GetEntries();
    cout << "** Chain contains " << allEntries << " events" << endl;

    GenParticle *particle;
    Electron *electron;
    Photon *photon;
    Muon *muon;

    //do i need all these ?
    Track *track;
    Tower *tower;
 
    Jet *jet;
    TObject *object;

    // Create the output file, tree and branches
    TFile *outfile = TFile::Open("outfile.root","RECREATE");
    TTree *outtree = new TTree("outtree", "outtree");

    // Define the parameters to be added
    Int_t iEvent;  
    Float_t j_pt;  
    Float_t j_eta;  
    Float_t j_phi;    
   
    Int_t j_btag;

    // i dont have jet.E info

    std::vector<float> part_E; 
    std::vector<float> part_px; 
    std::vector<float> part_py; 
    std::vector<float> part_pz;
    
    std::vector<int> part_PID;
    std::vector<int> part_Charge;  
    
    std::vector<float> track_D0;  
    std::vector<float> track_DZ;   
    std::vector<float> track_D0_sig;
    std::vector<float> track_DZ_sig;

    //******* Set branches
    outtree->Branch("br_iEvent", &iEvent, "iEvent/I");
    outtree->Branch("pt",&j_pt);
    outtree->Branch("eta",&j_eta);
    outtree->Branch("phi",&j_phi);

    outtree->Branch("btag",&j_btag);

    outtree->Branch("part_E", &part_E); 
    outtree->Branch("part_px", &part_px);
    outtree->Branch("part_py", &part_py);
    outtree->Branch("part_pz",&part_pz);
    
    outtree->Branch("part_PID",&part_PID);  
    outtree->Branch("part_Charge",&part_Charge);  

    outtree->Branch("track_d0",&track_D0);  
    outtree->Branch("track_dz",&track_DZ);

    outtree->Branch("track_d0_sig",&track_D0_sig);
    outtree->Branch("track_dz_sig",&track_DZ_sig);

    Long64_t entry;

    iEvent = 0;

    // Loop over all events
    for (unsigned long entry = 0; entry < 10000; ++entry)
    {
        // Load selected branches with data from specified event
        treeReader->ReadEntry(entry);
        iEvent++;
        cout << "##############################"<< endl;
        cout << "Event:" << iEvent << endl;


        Int_t numberOfEntries = branchJet->GetEntriesFast();

        // Loop over all jets in event
        for(int iJet = 0; iJet < numberOfEntries; ++iJet)
        {
            jet = (Jet*) branchJet->At(iJet);
            
            // Clear the vectors for each new jet
        
            part_E.clear(); 
            part_px.clear();
            part_py.clear();
            part_pz.clear();

            part_PID.clear();
            part_Charge.clear();

            track_D0.clear();
            track_DZ.clear();
            track_D0_sig.clear();
            track_DZ_sig.clear();


            j_pt = jet->PT;
            j_eta = jet->Eta;
            j_phi = jet->Phi;

            j_btag = jet->BTag;
       


            cout << "------------------------------"<< endl;
            cout << "Jet " << iJet << endl;
            cout << "Constituents Size: " << jet->Constituents.GetEntriesFast() << endl;

            int numberOfTracks = 0; 
            
            for(int iConstituent = 0; iConstituent < jet->Constituents.GetEntriesFast(); ++iConstituent)
            {
                object = jet->Constituents.At(iConstituent);
            
                if(object == 0)
                {
                    cout << "The constituent is not accesible!" << endl;
                    continue;
                }
                
                if(object->IsA() == Track::Class())
                {
                    numberOfTracks++;
                    track = (Track*) object;

                    part_PID.emplace_back(track->PID);
                    part_Charge.emplace_back(track->Charge);

                    track_D0.emplace_back(track->D0);
                    track_DZ.emplace_back(track->DZ);
                    track_D0_sig.emplace_back(track->ErrorD0);
                    track_DZ_sig.emplace_back(track->ErrorD0);
                
                    TRef particleRef = track->Particle; // Get the TRef object
                    particle = dynamic_cast<GenParticle*>(particleRef.GetObject()); // Retrieve the GenParticle object

                    if (particle != nullptr) 
                    {
                        part_E.emplace_back(particle->E);
                        part_px.emplace_back(particle->Px);
                        part_py.emplace_back(particle->Py);
                        part_pz.emplace_back(particle->Pz);
                    }
                }
            }
            cout << "Number of Tracks: " << numberOfTracks << endl;
            outtree->Fill();
        }
    }
    outfile->Write();
    delete outfile;
}
