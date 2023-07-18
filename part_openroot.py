import uproot

root_file_path = "/Users/asugu/delphes-master/outfile.root"
root_file = uproot.open(root_file_path)


tree_names = root_file.keys()
print(tree_names)

tree = root_file['outtree;1']


tree.show()

branch_iEvent = tree['br_iEvent']
branch_pt = tree["pt"]
branch_eta = tree["eta"]
branch_phi = tree["phi"]

branch_btag = tree["btag"]

branch_track_E = tree["part_E"]
branch_track_px = tree["part_px"] 
branch_track_py = tree["part_py"] 
branch_track_pz = tree["part_pz"] 

branch_track_PID = tree["part_PID"] 
branch_track_Charge = tree["part_Charge"]

branch_track_d0 = tree["track_d0"]
branch_track_dz = tree["track_dz"]
branch_track_d0_sig = tree["track_d0_sig"]
branch_track_dz_sig = tree["track_dz_sig"]


iEvent = branch_iEvent.array()
pt = branch_pt.array()
eta = branch_eta.array()
phi = branch_phi.array()

btag = branch_btag.array()

track_E = branch_track_E.array()
track_px = branch_track_px.array()
track_py = branch_track_py.array()
track_pz = branch_track_pz.array()

track_PID = branch_track_PID.array()
track_Charge = branch_track_Charge.array()

track_d0 = branch_track_d0.array()
track_dz = branch_track_dz.array()
track_d0_sig = branch_track_d0_sig.array()
track_dz_sig = branch_track_dz_sig.array()

"""
print(iEvent)
print(pt)
print(eta)
print(phi)

"""
""""for i in range(len(track_d0)):
    print(track_d0_sig[i])
    print(track_dz_sig[i])
"""

"""print(track_d0, "D0")

print(track_E,"E")
print(len(track_E),"E")
print(len(track_px),"px")
"""


track_len = 0
track_no = 0
for i in range(len(track_E)):
    if len(track_E[i]) != 0:
        track_len += len(track_E[i])
        track_no += 1
mean_track_len = track_len/track_no
print(f"Mean track number: {mean_track_len}")
print(f"Number of jets: {len(track_E)}")


no_btag = 0
for i in range(len(btag)):
    no_btag += btag[i] 

print(no_btag)




""""jet_events = []
for i, event_idx in enumerate(iEvent):
    jet_events.append({"event_index": event_idx, "track_pt": track_pt[i],"track_d0": track_d0[i]})

#print(jet_events)


"""

#df = tree.pandas.df()
#print(df)

#for i in range(len(track_PID)):
#    print(track_PID[i])