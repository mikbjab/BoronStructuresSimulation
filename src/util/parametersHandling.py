import csv
import json

# size -> Size of plate on which the experiment is conducted
# radius -> Size of sample in terms of size of the plate
# number_blue -> Number of blue dots on the plate
# steps -> Number of steps for evolution
# max_mut ->Max number of mutations per step

def save_configuration(size,radius,number_blue,steps,max_mut):
    data={"size":size,"radius":radius,"number_blue":number_blue,"steps":steps,"max_mut":max_mut}
    file_out=open("../../resources/parameters.json", "w")
    json.dump(data,file_out)

def load_configuration(filename):
    with open(filename,"r") as f:
        return json.load(f)

def save_param_config_csv(model, steps, signs,param_change,change,num_pre_step,param):
    with open("../../resources/param_table.csv","a") as file:
        writer=csv.writer(file)
        writer.writerow([model,num_pre_step,change,param_change,str(signs),steps,str(param)])