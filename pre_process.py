import pandas as pd
import numpy as np

from joblib import Parallel, delayed

def create_column_names():
    column_names = []

    column_names.append("jet_pt")
    column_names.append("jet_eta")
    column_names.append("jet_flavor")

    # high level trck variables
    names = ["trck_2_d0_sig", "trck_3_d0_sig",
            "trck_2_z0_sig", "trck_3_z0_sig",
            "n_trcks_over_d0_thrsld", "jet_prob", "jet_width_eta", 
            "jet_width_phi"]

    prefix = "hl_trck_var_"
    for name in names:
        column_names.append(prefix + name)


    names = ["vtx_sig", "n_secondary_vertices", "n_secondary_vtx_trcks",
            "delta_r_vtx", "vtx_mass", "vtx_energy_frac"]

    prefix = "hl_vtx_var_"
    for name in names:
        column_names.append(prefix + name)
        
    for i_track in range(15):
        prefix = "trck_vars_" + str(i_track) + "_"
        names = ["d0", "z0", "phi", "theta", "q_over_p", "d0d0", "z0d0", "z0z0", "phid0", 
                "phiz0", "phiphi", "thetad0", "thetaz0", "thetaphi", "thetatheta",
                "qoverpd0", "qoverpz0", "qoverpphi", "qoverptheta", "qoverpqoverp", 
                "trck_weight"]
        for name in names:
            column_names.append(prefix + name)
        
        prefix = "vtx_vars_" + str(i_track) + "_"
        names = ["mass", "displacement", "delta_eta_jet", "delta_phi_jet", 
                "displacement_sig", "n_trcks", "energy_frac"]
        for name in names:
            column_names.append(prefix + name)

    return column_names
    
column_names = create_column_names()

#print(column_names)

def process_jet_data(jet_data):
    
    flattened_data = []

    for i in range(3):
        flattened_data.append(jet_data[i])
    
    for i in range(8):
        flattened_data.append(jet_data[3][i])
    
    for i in range(6):
        flattened_data.append(jet_data[4][i])
    
    
    # track variables
    for i_track in range(15):
        
            for i_track_var in range(5):
                
                if i_track < len(jet_data[5]):
                    val = jet_data[5][i_track][0][i_track_var]  
                    if isinstance(val, float):
                        flattened_data.append(val)
                    else:
                        flattened_data.append(0)
                
                else:
                    flattened_data.append(0)
            
            
            for i_track_cov in range(15):
                
                if i_track < len(jet_data[5]):
                    val = jet_data[5][i_track][1][i_track_cov]  
                    if isinstance(val, float):
                        flattened_data.append(val)
                    else:
                        flattened_data.append(0)
                
                else:
                        flattened_data.append(0)
            
            if i_track < len(jet_data[5]):
                val = jet_data[5][i_track][2][0]
                if isinstance(val, float):
                    flattened_data.append(val)
                else:
                        flattened_data.append(0)
            
            else:
                flattened_data.append(0)
            
                
            for i_vtx_var in range(7):
                
                if i_track < len(jet_data[5]):
                    val = jet_data[5][i_track][3][i_vtx_var]
                    
                    if isinstance(val, float):
                        flattened_data.append(val)
                    else:
                        flattened_data.append(0)
            
                else:
                    flattened_data.append(0)
        

    return dict(zip(column_names, flattened_data))

chunksize = 10
chunks = pd.read_json(r'C:\Users\Asu\Desktop\jetclass\dataset.json', lines=True, chunksize = chunksize) 

num_lines = 11491971 #sum(1 for i in open("dataset.json", 'rb'))

def process_line(line):
    data = np.array(line)
    jet_data = process_jet_data(data)
    df  = pd.DataFrame.from_dict([jet_data])      
    return df


df = pd.DataFrame(columns=column_names, dtype="float")

quark_type = {"light_quark":0, "charm_quark":4, "bottom_quark":5}

selected_quark = "light_quark"
for i, chunk in enumerate(chunks):
    lines = chunk.to_numpy()
    new_lines = [line for line in lines if line[2]==quark_type[selected_quark]]
    
    #safeguard for empty content
    if len(new_lines)==0:
        continue   
    
    results = Parallel(n_jobs=len(new_lines), verbose=0)(delayed(process_line)(line) for line in new_lines)
      
    df = pd.concat([df, pd.concat(results, ignore_index = True)], ignore_index = True)
        #if i == 100:
        #    break
    
    
    if i%10==0:
    #    print(f"{i*chunksize}/{num_lines} ({100*i*chunksize/num_lines:.3f} %) events have been processed!", end="\r")
        print(f'No of selected type of quarks {len(df)}.', end='\r')
            
    if len(df)>50000:
        break

df.replace({"inf": 0, "-inf": 0}, inplace=True)
df.replace({"NaN": 0}, inplace=True)

#print(df)
df.to_csv('50000light.csv')
#df.to_hdf(f'data_{selected_quark}_jet.h5', key='df', mode='w')  

print('Finished')