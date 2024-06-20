import ROOT

def merge_histograms(file_path, chip_id):
    # Open the merged ROOT file
    file = ROOT.TFile(file_path)

    # Navigate through the directory structure
    base_path = f"Detector/Board_0/OpticalGroup_0/Hybrid_0/Chip_{chip_id}"

    # Retrieve the histograms
    hist_pixel_alive_1 = file.Get(f"{base_path}/D_B(0)_O(0)_H_(0)_PixelAlive_Chip({chip_id});1")
    hist_pixel_alive_2 = file.Get(f"{base_path}/D_B(0)_O(0)_H_(0)_PixelAlive_Chip({chip_id});2")

    # Check if histograms are successfully retrieved
    if not hist_pixel_alive_1 or not hist_pixel_alive_2:
        print("Error: Could not retrieve histograms")
        return

    # Create a new histogram to store the sum
    hist_pixel_alive_sum = hist_pixel_alive_1.Clone("PixelAlive_Sum")
    hist_pixel_alive_sum.Add(hist_pixel_alive_2)

    # Save the summed histogram to a new ROOT file
    output_file = ROOT.TFile("output.root", "RECREATE")
    hist_pixel_alive_sum.Write()
    output_file.Close()

    # Close the input file
    file.Close()

# Example usage
merge_histograms("/mnt/data/merged.root", 0)

