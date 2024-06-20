import ROOT
import sys

def plot_histogram(hist, title, chip_id, show_palette=False):
    canvas = ROOT.TCanvas(title, title, 800, 600)

    if show_palette:
        canvas.Update()
        palette = hist.GetListOfFunctions().FindObject("palette")
        if palette:
            palette.SetX1NDC(0.90)
            palette.SetX2NDC(0.94)
            palette.SetY1NDC(0.1)
            palette.SetY2NDC(0.9)
            palette.Draw()
    hist.Draw("COLZ")

    # Adjust the z-axis (color scale) range
    if "PixelAlive" in title:
        hist.SetMinimum(0.0)  # Set the minimum value for the color scale
        hist.SetMaximum(2E-6)  # Set the maximum value for the color scale
        hist.Draw("COLZ")
    elif "ToT" in title:
        hist.SetMinimum(0.0)  # Set the minimum value for the color scale
        hist.SetMaximum(15)  # Set the maximum value for the color scale
        hist.Draw("COLZ")

    canvas.Update()
    # Disable stats
    stats = hist.GetListOfFunctions().FindObject("stats")
    if stats:
        print("stats exist")
        stats.SetOptStat(0)  # Disable statistics display
    #canvas.Update()
    #hist.SetMinimum(1E-7)  # Set the minimum value for the color scale
    #hist.SetMaximum(1E-6)  # Set the maximum value for the color scale
    #canvas.Modified()
    #canvas.Update()
    canvas.SaveAs(f"{title}_Chip({chip_id}).pdf")
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
            plot_histogram(hist, f"{hist_name}_Histogram_{idx+1}", chip_id)
        plot_histogram(hist_sum, f"Merged_{hist_name}_Histogram", chip_id, show_palette=True)



        # Save the summed histogram to a new ROOT file
        output_file = ROOT.TFile(f"output_{hist_name}.root", "RECREATE")
        hist_sum.Write()
        output_file.Close()



    # Close the input file
    file.Close()


# Check if arguments are provided
if len(sys.argv) < 2:
    print("Usage: python script.py arg1 arg2 ...")
    sys.exit(1)

merged_root_file = sys.argv[1]
chip_id = sys.argv[2]
merge_histograms(sys.argv[1], sys.argv[2], ["PixelAlive","ToT2D"])

#merge_histograms("merged.root", 0, ["PixelAlive", "ToT2D"])

file_output = ROOT.TFile("output_PixelAlive.root")
hist_sum = file_output.Get("PixelAlive_Sum")
Map2 = ROOT.TH2F(f"Pixels with 0 hits Chip({chip_id})", f"Pixels with 0 hits Chip({chip_id})", 432, 1, 433, 336, 1,337)
number_of_hits_histo = ROOT.TH1F(f"Number of hits per pixel Chip({chip_id}", f"Number of hits per pixel Chip({chip_id}",
                                 100, 0, 1000)
for i in range(1, 337):
    for j in range(1, 433):
        if ((j < 81) | (j > 104)):
            occupancy = hist_sum.GetBinContent(j, i)
            hit_per_pixel = 10 * occupancy * 1.0E+07
            print("Number of hits", hit_per_pixel)
            # Create the histogram
            number_of_hits_histo.Fill(hit_per_pixel)

        if hist_sum.GetBinContent(j, i) == 0:
            print("Detached:", j, i, hist_sum.GetBinContent(j, i))
            #if ((j >= 81) & (j <= 104)):
            #    continue
            Map2.Fill(j, i, 1)


# plot_histogram(Map2, f"Disconnected_pixels", show_palette=True)
c = ROOT.TCanvas()
# Set the fill color for the bins to red
Map2.SetFillColor(ROOT.kRed)
Map2.SetMarkerStyle(20)  # Optional: set marker style, 20 is a filled circle
Map2.GetXaxis().SetTitle("col")
Map2.GetYaxis().SetTitle("row")
Map2.Draw("BOX")  # Draw bins as colored boxes
# Update the canvas to make sure the histogram is drawn
c.Update()
# Get the statistics box
stats = Map2.GetListOfFunctions().FindObject("stats")
if stats:
    stats.SetOptStat(10)  # Customize stats box: 1 for entries, 1 for mean, 1 for standard deviation, 0 for others
    stats.SetX1NDC(0.75)  # Set x start position (Normalized Device Coordinates)
    stats.SetX2NDC(0.90)  # Set x end position (Normalized Device Coordinates)
    stats.SetY1NDC(0.90)  # Set y start position (Normalized Device Coordinates)
    stats.SetY2NDC(0.95)  # Set y end position (Normalized Device Coordinates)
    stats.SetTextSize(0.03)  # Set text size (0.03 is an example, adjust as needed)
c.SaveAs(f"disconnected_pixels_Chip({chip_id}).pdf")

# Set titles for the axes
number_of_hits_histo.GetXaxis().SetTitle("Number of Hits")
number_of_hits_histo.GetYaxis().SetTitle("Entries")
# Set the title of the histogram
number_of_hits_histo.SetTitle(f"Number of hits per pixel Chip({chip_id}")

# Draw the histogram
c2 = ROOT.TCanvas("c2", f"Number of hits per pixel Chip({chip_id}", 800, 600)
c2.SetLogy()  # Set the y-axis to a logarithmic scale
number_of_hits_histo.Draw()

# Save the histogram to a file
c2.SaveAs(f"number_of_hits_histo_Chip({chip_id}.pdf")