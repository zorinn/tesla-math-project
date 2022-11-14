import car_funcs

DELTA_T = 0.01

def euler_method(v,car):
    
    v_n_plus_1 = v + (car_funcs.H_of_v(v,car)*DELTA_T)
    return v_n_plus_1


def main():

    tesla_model_s_p100d = car_funcs.Car(2250,0.24,14.15,1.11,2.1,980,450.4,4000,5750,150,16614)

    v_dict = {}
    v = 0
    
    for i in range(20000):
        v1 = euler_method(v,tesla_model_s_p100d)
        v_dict[i] = v1
        v = v1

    print(v_dict)

if __name__ == "__main__":
    main()