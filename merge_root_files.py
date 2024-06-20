import ROOT
def plot_histogram(hist, title):
    canvas = ROOT.TCanvas(title, title, 800, 600)
    hist.Draw("COLZ")
    canvas.SaveAs(f"{title}.pdf")
    canvas.Draw()


def merge_histograms(file_path, chip_id):
    # Open the merged ROOT file
    file = ROOT.TFile(file_path)

    # Navigate through the directory structure
    base_path = f"Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_{chip_id}"

    # Retrieve the canvases
    canvas_pixel_alive_1 = file.Get(f"{base_path}/D_B(0)_O(0)_H(0)_PixelAlive_Chip({chip_id});1")
    canvas_pixel_alive_2 = file.Get(f"{base_path}/D_B(0)_O(0)_H(0)_PixelAlive_Chip({chip_id});2")

    # Check if canvases are successfully retrieved
    if not canvas_pixel_alive_1 or not canvas_pixel_alive_2:
        print("Error: Could not retrieve canvases")
        return

    # Retrieve the histograms from the canvases
    hist_pixel_alive_1 = canvas_pixel_alive_1.GetPrimitive(f"D_B(0)_O(0)_H(0)_PixelAlive_Chip({chip_id})")
    hist_pixel_alive_2 = canvas_pixel_alive_2.GetPrimitive(f"D_B(0)_O(0)_H(0)_PixelAlive_Chip({chip_id})")

    tot_1 = canvas_pixel_alive_1.GetPrimitive(f"D_B(0)_O(0)_H(0)_TOT2D_Chip({chip_id})")
    tot_2 = canvas_pixel_alive_2.GetPrimitive(f"D_B(0)_O(0)_H(0)_TOT2D_Chip({chip_id})")
    # Check if histograms are successfully retrieved from the canvases
    if not hist_pixel_alive_1 or not hist_pixel_alive_2:
        print("Error: Could not retrieve histograms from the canvases")
        return

    # Create a new histogram to store the sum
    hist_pixel_alive_sum = hist_pixel_alive_1.Clone("PixelAlive_Sum")
    hist_pixel_alive_sum.Add(hist_pixel_alive_2)

    # Plot the histograms
    plot_histogram(hist_pixel_alive_1, "PixelAlive_Histogram_1")
    plot_histogram(hist_pixel_alive_2, "PixelAlive_Histogram_2")
    plot_histogram(hist_pixel_alive_sum, "Merged_PixelAlive_Histogram")

    # Save the summed histogram to a new ROOT file
    output_file = ROOT.TFile("output.root", "RECREATE")
    hist_pixel_alive_sum.Write()
    output_file.Close()

    # Close the input file
    file.Close()

# Example usage
merge_histograms("merged.root", 1)

