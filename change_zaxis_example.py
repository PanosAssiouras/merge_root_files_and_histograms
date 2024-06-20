import ROOT
import random


# Create a 2D histogram filled with random values
def create_random_histogram():
    hist = ROOT.TH2F("random_hist", "Random 2D Histogram", 100, 0, 100, 100, 0, 100)
    for i in range(100):
        for j in range(100):
            hist.Fill(i, j, random.uniform(0, 1))  # Fill with random values between 0 and 1
    return hist


# Plot and save the histogram with adjusted color scale
def plot_histogram(hist, title, z_min=None, z_max=None):
    canvas = ROOT.TCanvas(title, title, 800, 600)

    # Adjust the z-axis (color scale) range if specified
    if z_min is not None:
        hist.SetMinimum(z_min)  # Set the minimum value for the color scale
    if z_max is not None:
        hist.SetMaximum(z_max)  # Set the maximum value for the color scale

    hist.Draw("COLZ")

    canvas.Update()
    canvas.SaveAs(f"{title}.pdf")
    canvas.Draw()


# Main function to demonstrate
def main():
    # Create a random 2D histogram
    hist = create_random_histogram()

    # Plot the histogram with adjusted z-axis range
    plot_histogram(hist, "Random_Histogram", z_min=0.2, z_max=0.8)


# Run the main function
if __name__ == "__main__":
    ROOT.gROOT.SetBatch(True)  # Enable batch mode to suppress GUI
    main()
