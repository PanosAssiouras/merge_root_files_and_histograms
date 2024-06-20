#include <TFile.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TFileMerger.h>
#include <TKey.h>
#include <TSystem.h>
#include <iostream>
#include <string>
#include <vector>

void MergePixelaliveHistograms(const std::vector<std::string>& files) {
    // Create a new ROOT file to store the merged histograms
    TFileMerger merger;
    merger.OutputFile("Merged_NoiseScan.root");

    // Add input files to the merger
    for (const auto& file : files) {
        merger.AddFile(file.c_str());
    }

    // Merge the files
    merger.Merge();

    // Open the merged file
    TFile* merged_file = TFile::Open("Merged_NoiseScan.root");
    if (!merged_file || merged_file->IsZombie()) {
        std::cerr << "Error opening merged file: Merged_NoiseScan.root" << std::endl;
        return;
    }

    // List of histogram names to be plotted (modify if needed)
    std::vector<std::string> hist_names = {
        "D_B(0)_O(0)_H(0)_PixelAlive_Chip(0)"
    };

    // Plot each histogram
    for (const auto& hist_name : hist_names) {
        TH2F* hist = (TH2F*)merged_file->Get(hist_name.c_str());
        if (!hist) {
            std::cerr << "Error: Histogram '" << hist_name << "' not found in merged file." << std::endl;
            continue;
        }

        TCanvas* canvas = new TCanvas(("canvas_" + hist_name).c_str(), hist_name.c_str(), 800, 600);
        hist->Draw("COLZ");
        canvas->Update();
        canvas->SaveAs((hist_name + ".png").c_str());

        // Keep the canvas open
        canvas->Connect("Closed()", "TApplication", gApplication, "Terminate()");
    }

    merged_file->Close();
    delete merged_file;
}

void RunMerge() {
    std::vector<std::string> files = {
        "Run000006_NoiseScan.root",
        "Run000009_NoiseScan.root"
    };
    MergePixelaliveHistograms(files);
}

