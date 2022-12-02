import car_funcs
import csv
import math
import numpy

DELTA_T = 0.01
TIMES_AND_VELOCITY_DATA = {
    0:0,
    0.26:5.9,
    1.46:31.1,
    2.26:49.7,
    3.16:62.1,
    4.06:74.6,
    4.56:80.8,
    7.46:99.4,
    9.26:111.8,
    11.66:124.3,
    18.66:149.1
}
TAU_LIST = list(numpy.arange(1.30,2.01,.01))

def euler_method_h_of_v(v,car):
    
    v_n_plus_1 = v + car_funcs.H_of_v(v,car)*DELTA_T
    return v_n_plus_1

def euler_method_T_of_r(v,tau,car):
    
    v_n_plus_1 = v + car_funcs.H_of_v_torque(v,tau,car)*DELTA_T
    return v_n_plus_1

def write_to_csv(csv_file,data):
    csv_headers = ['seconds','velocity']

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_headers)
        writer.writeheader()
        for dict_data in data:
            writer.writerow(dict_data)

def find_RMSE(v_data):
    sum = 0

    for key in TIMES_AND_VELOCITY_DATA:
        # print(v_data[int(key*100)])
        # print(data['velocity'])
        # print(data)

        data = v_data[round(key*100)]
        sum += (TIMES_AND_VELOCITY_DATA[key] - data['velocity'])**2
    
    return math.sqrt(sum)

def generate_data_old(car):
    v_data = []
    v = 0

    start_dict = {}
    start_dict['seconds'] = 0
    start_dict['velocity'] = 0
    v_data.append(start_dict)
    
    for i in range(2000):
        v_dict = {}
        v1 = euler_method_h_of_v(v,car)
        v_dict['seconds'] = (i+1) / 100
        v_dict['velocity'] = v1 * 2.23694 # meters per second to mph
        v_data.append(v_dict)
        v = v1   
    
    return v_data

def get_tau_RMSE_data(tau,car):
    v_data = []
    v = 0

    start_dict = {}
    start_dict['seconds'] = 0
    start_dict['velocity'] = 0
    v_data.append(start_dict)
    
    for i in range(2000):
        v_dict = {}
        v1 = euler_method_T_of_r(v,tau,car)
        v_dict['seconds'] = (i+1) / 100
        v_dict['velocity'] = v1 * 2.23694 # meters per second to mph
        v_data.append(v_dict)
        v = v1  

    return find_RMSE(v_data)

def main():

    tesla_model_s_p100d = car_funcs.Car(2250,0.24,(14.15*0.0254),1.11,2.1,980,450.4,4000,5750,150,16614)

    # tesla_model_s_data_no_torque_factor = generate_data_old(tesla_model_s_p100d)

    # write_to_csv('tesla_model_s_no_torque_factor.csv',tesla_model_s_data)
    # print(v_data)
    # print(find_RMSE(tesla_model_s_data))
    # print(TAU_LIST)

    for tau in TAU_LIST:
        rounded_index = round(tau,2)
        tau_RMSE_data = get_tau_RMSE_data(tau,tesla_model_s_p100d)
        print(tau_RMSE_data)

if __name__ == "__main__":
    main()