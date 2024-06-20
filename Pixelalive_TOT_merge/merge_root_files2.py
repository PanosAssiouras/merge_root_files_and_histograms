import ROOT

def plot_histogram(hist, title, show_palette=False):
    canvas = ROOT.TCanvas(title, title, 800, 600)
    if show_palette:
        hist.Draw("COLZ")
    else:
        hist.Draw("COLZ")
    canvas.Update()
    canvas.SaveAs(f"{title}.pdf")
    canvas.Draw()

def merge_histograms(file_path, chip_id, histogram_names):
    # Open the merged ROOT file
    file = ROOT.TFile(file_path)

    # Navigate through the directory structure
    base_path = f"Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_{chip_id}"

    for hist_name in histogram_names:
        histograms = []
        for i in range(1, 10):  # Adjust the range based on the number of histograms you have
            hist_path = f"{base_path}/D_B(0)_O(0)_H(0)_{hist_name}_Chip({chip_id});{i}"
            canvas = file.Get(hist_path)
            if canvas:
                hist = canvas.GetPrimitive(f"D_B(0)_O(0)_H(0)_{hist_name}_Chip({chip_id})")
                if hist:
                    histograms.append(hist)

        if not histograms:
            print(f"Error: Could not retrieve histograms for {hist_name}")
            continue

        # Merge the histograms
        hist_sum = histograms[0].Clone(f"{hist_name}_Sum")
        for hist in histograms[1:]:
            hist_sum.Add(hist)

        # Plot the histograms
        for idx, hist in enumerate(histograms):
            plot_histogram(hist, f"{hist_name}_Histogram_{idx+1}")
        plot_histogram(hist_sum, f"Merged_{hist_name}_Histogram", show_palette=True)

        # Save the summed histogram to a new ROOT file
        output_file = ROOT.TFile(f"output_{hist_name}.root", "RECREATE")
        hist_sum.Write()
        output_file.Close()

    # Close the input file
    file.Close()

# Example usage
merge_histograms("merged.root", 0, ["PixelAlive", "ToT2D"])

