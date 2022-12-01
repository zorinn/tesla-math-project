import car_funcs
import csv

DELTA_T = 0.01

def euler_method(v,car):
    
    v_n_plus_1 = v + car_funcs.H_of_v(v,car)*DELTA_T
    return v_n_plus_1

def write_to_csv(csv_file,data):
    csv_headers = ['miniseconds','velocity']

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_headers)
        writer.writeheader()
        for dict_data in data:
            writer.writerow(dict_data)


def main():

    tesla_model_s_p100d = car_funcs.Car(2250,0.24,(14.15*0.0254),1.11,2.1,980,450.4,4000,5750,150,16614)

    v_data = []
    v = 0
    
    for i in range(2000):
        v_dict = dict()
        v1 = euler_method(v,tesla_model_s_p100d)
        v_dict['miniseconds'] = i
        v_dict['velocity'] = v1 * 2.23694 # meters per second to mph
        v_data.append(v_dict)
        v = v1

    write_to_csv('tesla_model_s_no_torque_factor.csv',v_data)

if __name__ == "__main__":
    main()