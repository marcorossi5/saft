from saft.saft import SAF_File


fname = "examples/histos.saf"
saf_file_1 = SAF_File(fname)
saf_file_2 = SAF_File(fname)

# get histogram by title
h1 = saf_file_1.get_from_title("PT")
h2 = saf_file_2.get_from_title("PT")

print("Adding histograms", h1 + h2)
print("Subtracting histograms", h1 - h2)
print("Multiplying histograms", h1 * h2)
