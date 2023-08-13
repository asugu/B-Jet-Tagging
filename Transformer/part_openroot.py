import uproot3 as uproot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import awkward as ak

import pickle


def pad_array(array, target_length, default_value=0):
    if len(array) >= target_length:
        return array[:target_length]
    return np.pad(array, (0, target_length - len(array)), constant_values=default_value)

root_file_path = "/home/asugu/work/part/outfile_true_1m.root"
root_file = uproot.open(root_file_path)

tree_names = root_file.keys()
print(tree_names)

tree = root_file['outtree;11']

branch_iEvent = tree['br_iEvent']
branch_pt = tree["jet_pt"]
branch_eta = tree["jet_eta"]
branch_phi = tree["jet_phi"]
branch_E = tree["jet_E"]

branch_btag = tree["btag"]

branch_track_E = tree["part_E"]
branch_track_px = tree["part_px"] 
branch_track_py = tree["part_py"] 
branch_track_pz = tree["part_pz"] 

branch_track_pt = tree["part_pt"] 
branch_track_eta = tree["part_eta"] 
branch_track_phi = tree["part_phi"] 

branch_track_PID = tree["part_PID"] 
branch_track_Charge = tree["part_Charge"]

branch_track_d0 = tree["track_d0"]
branch_track_dz = tree["track_dz"]
branch_track_d0_sig = tree["track_d0_sig"]
branch_track_dz_sig = tree["track_dz_sig"]

branch_track_pt = tree["part_pt"] 

iEvent = ak.Array(branch_iEvent.array())
jet_pt = ak.Array(branch_pt.array())
jet_eta = ak.Array(branch_eta.array())
jet_phi = ak.Array(branch_phi.array())
jet_E = ak.Array(branch_E.array())
jet_btag = ak.Array(branch_btag.array())
unsorted_track_E = ak.Array(branch_track_E.array())
unsorted_track_px = ak.Array(branch_track_px.array())
unsorted_track_py = ak.Array(branch_track_py.array())
unsorted_track_pz = ak.Array(branch_track_pz.array())
unsorted_track_pt = ak.Array(branch_track_pt.array())
unsorted_track_eta = ak.Array(branch_track_eta.array())
unsorted_track_phi = ak.Array(branch_track_phi.array())
unsorted_track_PID = ak.Array(branch_track_PID.array())
unsorted_track_Charge = ak.Array(branch_track_Charge.array())
unsorted_track_d0 = ak.Array(branch_track_d0.array())
unsorted_track_dz = ak.Array(branch_track_dz.array())
unsorted_track_d0_sig = ak.Array(branch_track_d0_sig.array())
unsorted_track_dz_sig = ak.Array(branch_track_dz_sig.array())
unsorted_track_pt = ak.Array(branch_track_pt.array())
                             
print("hey hey")

no_btag = 0
for i in range(len(jet_btag)):
    no_btag += jet_btag[i] 

print(no_btag,"number of b_tags")

print(len(jet_btag))

sorted_indices = ak.argsort(unsorted_track_E, axis=1, ascending=False,stable=True)

track_E = ak.Array([
    [unsorted_track_E[i][sorted_indices[i][j]] for j in range(len(unsorted_track_E[i]))]
    for i in range(len(unsorted_track_E))
])

track_px = ak.Array([
    [unsorted_track_px[i][sorted_indices[i][j]] for j in range(len(unsorted_track_px[i]))]
    for i in range(len(unsorted_track_px))
])

track_py = ak.Array([
    [unsorted_track_py[i][sorted_indices[i][j]] for j in range(len(unsorted_track_py[i]))]
    for i in range(len(unsorted_track_py))
])

track_pz = ak.Array([
    [unsorted_track_pz[i][sorted_indices[i][j]] for j in range(len(unsorted_track_pz[i]))]
    for i in range(len(unsorted_track_pz))
])

track_pt = ak.Array([
    [unsorted_track_pt[i][sorted_indices[i][j]] for j in range(len(unsorted_track_pt[i]))]
    for i in range(len(unsorted_track_pt))
])

track_eta = ak.Array([
    [unsorted_track_eta[i][sorted_indices[i][j]] for j in range(len(unsorted_track_eta[i]))]
    for i in range(len(unsorted_track_eta))
])

track_phi = ak.Array([
    [unsorted_track_phi[i][sorted_indices[i][j]] for j in range(len(unsorted_track_phi[i]))]
    for i in range(len(unsorted_track_phi))
])

track_PID = ak.Array([
    [unsorted_track_PID[i][sorted_indices[i][j]] for j in range(len(unsorted_track_PID[i]))]
    for i in range(len(unsorted_track_PID))
])

track_Charge = ak.Array([
    [unsorted_track_Charge[i][sorted_indices[i][j]] for j in range(len(unsorted_track_Charge[i]))]
    for i in range(len(unsorted_track_Charge))
])

track_d0 = ak.Array([
    [unsorted_track_d0[i][sorted_indices[i][j]] for j in range(len(unsorted_track_d0[i]))]
    for i in range(len(unsorted_track_d0))
])

track_dz = ak.Array([
    [unsorted_track_dz[i][sorted_indices[i][j]] for j in range(len(unsorted_track_dz[i]))]
    for i in range(len(unsorted_track_dz))
])

track_d0_sig = ak.Array([
    [unsorted_track_d0_sig[i][sorted_indices[i][j]] for j in range(len(unsorted_track_d0_sig[i]))]
    for i in range(len(unsorted_track_d0_sig))
])

track_dz_sig = ak.Array([
    [unsorted_track_dz_sig[i][sorted_indices[i][j]] for j in range(len(unsorted_track_dz_sig[i]))]
    for i in range(len(unsorted_track_dz_sig))
])




jet_count = []
for i in range(len(track_pt)):
    jet_count.append(len(track_pt[i]))


non_empty_track_indices = [i for i, track in enumerate(track_E) if len(track) > 0]

max_track_length = 50  #max(len(track) for track in track_E)

track_E = [pad_array(track, max_track_length) for track in track_E]
track_px = [pad_array(track, max_track_length) for track in track_px]
track_py = [pad_array(track, max_track_length) for track in track_py]
track_pz = [pad_array(track, max_track_length) for track in track_pz]
track_pt = [pad_array(track, max_track_length) for track in track_pt]
track_eta = [pad_array(track, max_track_length) for track in track_eta]
track_phi = [pad_array(track, max_track_length) for track in track_phi]
track_PID = [pad_array(track, max_track_length) for track in track_PID]
track_Charge = [pad_array(track, max_track_length) for track in track_Charge] 
track_d0 = [pad_array(track, max_track_length) for track in track_d0]
track_dz = [pad_array(track, max_track_length) for track in track_dz]
track_d0_sig = [pad_array(track, max_track_length) for track in track_d0_sig]
track_dz_sig = [pad_array(track, max_track_length) for track in track_dz_sig]



event_data = []
for i in non_empty_track_indices:
    event_dict = {
        'iEvent': iEvent[i],
        'jet_pt': jet_pt[i],
        'jet_eta': jet_eta[i],
        'jet_phi': jet_phi[i],
        'jet_E': jet_E[i],
        'btag': jet_btag[i],
        'jet_count': jet_count[i],
        'part_E': np.array(track_E[i], dtype=np.float32),
        'part_px': np.array(track_px[i], dtype=np.float32),
        'part_py': np.array(track_py[i], dtype=np.float32),
        'part_pz': np.array(track_pz[i], dtype=np.float32),
        'part_PID': np.array(track_PID[i], dtype=np.float32),
        'part_Charge': np.array(track_Charge[i], dtype=np.float32),
        'track_d0': np.array(track_d0[i], dtype=np.float32),
        'track_dz': np.array(track_dz[i], dtype=np.float32),
        'track_d0_sig': np.array(track_d0_sig[i], dtype=np.float32),
        'track_dz_sig': np.array(track_dz_sig[i], dtype=np.float32),
        'part_pt': np.array(track_pt[i], dtype=np.float32)
    }
    event_data.append(event_dict)



file_path = 'event_data_true_1m.pkl'

# Write event_data to the file using pickle
with open(file_path, 'wb') as file:
    pickle.dump(event_data, file)


#df = pd.DataFrame(event_data)

#print(df["part_E"][0])

#print(df["part_pt"][0])


#df.to_hdf(f'sorted_ttbar.hdf5', key='df', mode='w')  



#df.to_csv('sorted_padded_ttbar.csv', index=False)  



"""
if all(len(track_E[i]) == len(track_px[i]) == len(track_py[i]) == len(track_pz[i]) == len(track_PID[i]) == len(track_Charge[i]) == len(track_d0[i]) == len(track_d0_sig[i]) == len(track_dz[i]) == len(track_dz_sig[i]) == len(track_pt[i]) for i in range(len(track_E))):
    print("All lengths match for all 55000 elements.")
else:
    print("Lengths do not match for all 55000 elements.")

    




print("Unsorted track_pt:", unsorted_track_pt[0])
print("Sorted track_pt:", track_pt[0])

# Check if the arrays are sorted correctly
print("Is sorted_track_pt in descending order?", all(track_pt[0, i] >= track_pt[0, i+1] for i in range(len(track_pt[0])-1)))
print("Sorted indices:", sorted_indices[0])
for j in range(len(track_pt)):
    for i in range(len(track_pt[j]) - 1):
        if track_pt[j, i] < track_pt[j, i+1]:
            print("track_pt is not sorted correctly.")
            break
else:
    print("track_pt is sorted correctly.")



    



track_len = 0
track_no = 0
max_length = 0
long_count = 0
length_cut = 80
long_indexes =[]
for i in range(len(track_E)):
    if len(track_E[i]) != 0:
        track_len += len(track_E[i])
        track_no += 1
    current_length = len(track_E[i])
   
    if current_length > length_cut:
        long_count += 1
        long_indexes.append(i)

    if current_length > max_length:
        max_length = current_length
mean_track_len = track_len/track_no
print(f"Mean track number: {mean_track_len}")
print(f"Number of jets: {len(track_E)}")
print(f"max track len:{max_length}")
print(f"Percentage of cuts {1-(long_count/len(track_E))}")

no_btag = 0
for i in range(len(btag)):
    no_btag += btag[i] 

print(no_btag,"number of b_tags")

long_b_count = 0
for i in long_indexes:
    long_b_count += btag[i]
print(long_b_count,"number of cut b-jets")
print(long_b_count/no_btag,"percentage of discarded b_jets")
print(length_cut,"cut length")
lengths = [len(element) for element in track_E]

plt.hist(lengths, bins=20, edgecolor='black')

# Customize the plot (optional)
plt.title('Track Number')
plt.xlabel('Value')
plt.ylabel('Frequency')

# Display the plot
#plt.show()
"""

