#include <TFile.h>
#include <TH1.h>
#include <TCanvas.h>
#include <TLegend.h>
#include <TKey.h>
#include <TSystem.h>
#include <iostream>
#include <string>
#include <map>

void MergePixelaliveHistograms() {
    // List of input ROOT files
    std::string input_files[] = {
        "Run000006_NoiseScan.root",
        "Run000009_NoiseScan.root"
    };
    const int n_files = 2;

    // Create a new ROOT file to store the merged histograms
    TFile* output_file = TFile::Open("/mnt/data/Merged_NoiseScan.root", "RECREATE");

    // Initialize dictionary to hold histograms
    std::map<std::string, TH1*> histograms;

    // Loop over all input files
    for (int i = 0; i < n_files; ++i) {
        TFile* input_file = TFile::Open(input_files[i].c_str());

        // Get the list of keys (histograms) in the input file
        TIter next(input_file->GetListOfKeys());
        TKey* key;

        // Loop over all keys to find Pixelalive histograms
        while ((key = (TKey*)next())) {
            TObject* obj = key->ReadObj();
            if (obj->IsA()->InheritsFrom("TH1") && std::string(obj->GetName()).find("Pixelalive") != std::string::npos) {
                TH1* hist = (TH1*)obj;
                std::string hist_name = hist->GetName();
                
                if (histograms.find(hist_name) == histograms.end()) {
                    // Clone the histogram into the output file
                    TH1* hist_clone = (TH1*)hist->Clone();
                    histograms[hist_name] = hist_clone;
                } else {
                    // Add the histogram to the existing one
                    histograms[hist_name]->Add(hist);
                }
            }
        }

        input_file->Close();
        delete input_file;
    }

    // Save and close the merged histograms in the output file
    for (auto& hist_pair : histograms) {
        hist_pair.second->SetDirectory(output_file);
        hist_pair.second->Write();
    }
    output_file->Close();
    delete output_file;

    std::cout << "Pixelalive histograms merged and saved in 'Merged_NoiseScan.root'." << std::endl;
}

// Execute the function
void RunMerge() {
    MergePixelaliveHistograms();
}

