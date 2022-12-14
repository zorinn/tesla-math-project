import car_funcs
import csv
import math
import numpy

DELTA_T = 0.01
TIMES_AND_VELOCITY_DATA_P100 = {
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
TIMES_AND_VELOCITY_DATA_CHIRON = {
    0:0,
    0.2:5,
    2.6:60,
    4.6:100,
    6.7:130,
    8.8:150,
    15.9:200,
    42.2:249
}
TAU_LIST = list(numpy.arange(1.30,2.01,.01))

def euler_method_h_of_v(v,car):
    
    v_n_plus_1 = v + car_funcs.H_of_v(v,car)*DELTA_T
    return v_n_plus_1

def euler_method_T_of_r(v,tau,car):
    
    v_n_plus_1 = v + car_funcs.H_of_v_torque(v,tau,car)*DELTA_T
    return v_n_plus_1

def write_to_csv(csv_file,data,csv_headers):

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=csv_headers)
        writer.writeheader()
        for dict_data in data:
            writer.writerow(dict_data)

def find_RMSE(v_data,data_dict):
    sum = 0

    for key in data_dict:
        # print(v_data[int(key*100)])
        # print(data['velocity'])
        # print(data)

        data = v_data[round(key*100)]
        sum += (data_dict[key] - data['velocity'])**2
    
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

    return find_RMSE(v_data,TIMES_AND_VELOCITY_DATA_P100)

def generate_data_new(car,seconds):
    tau = 1.55
    v_data = []
    v = 0

    start_dict = {}
    start_dict['seconds'] = 0
    start_dict['velocity'] = 0
    v_data.append(start_dict)
    
    for i in range(seconds*100):
        v_dict = {}
        v1 = euler_method_T_of_r(v,tau,car)
        v_dict['seconds'] = (i+1) / 100
        v_dict['velocity'] = v1 * 2.23694 # meters per second to mph
        v_data.append(v_dict)
        v = v1  

    return v_data


def main():

    tesla_model_s_p100d = car_funcs.Car(2250,0.24,(14.15*0.0254),1.11,2.1,980,450.4,4000,5750,150,16614)

    tesla_model_s_data_no_torque_factor = generate_data_old(tesla_model_s_p100d) # this generates simulated velocity data without empirical torque factor

    """
    Writing Tesla Model S P100D data to csv and also finding RMSE for simulated data vs actual data
    """
    # write_to_csv('tesla_model_s_no_torque_factor.csv',tesla_model_s_data_no_torque_factor,['seconds','velocity'])
    # print(find_RMSE(tesla_model_s_data_no_torque_factor,TIMES_AND_VELOCITY_DATA_P100))

    """
    Iterates through tau in 1.3 <= tau <= 2, and writes RMSE for each tau to csv.
    This helps me find the ideal tau value for the new method involving the empirical torque factor.
    """
    # print(TAU_LIST)
    # tau_RMSE_list = []
    # for tau in TAU_LIST:
    #     tau_RMSE_dict = {}
    #     rounded_tau = round(tau,2)
    #     print(rounded_tau)
    #     tau_RMSE_data = get_tau_RMSE_data(tau,tesla_model_s_p100d)
    #     print(tau_RMSE_data)
    #     tau_RMSE_dict['tau'] = rounded_tau
    #     tau_RMSE_dict['RMSE'] = tau_RMSE_data
    #     tau_RMSE_list.append(tau_RMSE_dict)
    # write_to_csv('tau_RMSE_data.csv',tau_RMSE_list,['tau','RMSE'])

    """
    Makes new Tesla Model S P100D based off of ideal tau value and new functions implementing the empirical torque factor. Then, it puts data in csv file.
    Also finds RMSE using new data.
    """
    tesla_model_s_data_torque_factor = generate_data_new(tesla_model_s_p100d,20) # this generates tesla model s p100 data with empirical torque factor
    # write_to_csv('tesla_model_s_torque_factor.csv',tesla_model_s_data_torque_factor,['seconds','velocity'])
    # print(find_RMSE(tesla_model_s_data_torque_factor,TIMES_AND_VELOCITY_DATA_P100))

    """
    Simulates velocity data with Tesla Roadster using new method and puts data into csv file.
    Finds RMSE by comparing simulated Tesla Roadster data with actual data from the Bugatti Chiron.
    """
    tesla_roadster = car_funcs.Car(2000,0.36,(14.35*0.0254),1.27,2.072,1072,1000,8907,8907,250,27690)
    tesla_roadster_data = generate_data_new(tesla_roadster,45)
    write_to_csv('tesla_roadster_data.csv',tesla_roadster_data,['seconds','velocity'])
    print(find_RMSE(tesla_roadster_data,TIMES_AND_VELOCITY_DATA_CHIRON))

if __name__ == "__main__":
    main()