import math

class Car:

    def __init__(self, mass, drag_coefficient, tire_radius, static_friction, surface_area,
                    t_max, p_max, r_1, r_2, max_velocity, r_max)
        
        self.gravitational_acceleration = 9.81
        self.air_density = 1.2041
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.tire_radius = tire_radius
        self.static_friction = friction
        self.surface_area = surface_area
        self.gear_reduction = 9.325
        self.t_max = t_max
        self.p_max = p_max
        self.r_1 = r_1
        self.r_2 = r_2
        self.max_velocity = max_velocity
        self.r_max = r_max

def find_R(v,car):
    return (60*car.gear_reduction*v)/(2*math.pi*car.tire_radius)

def f_m_of_R(R,car):

    if R <= car.r_1:
        result = (car.gear_reduction*car.t_max) / car.tire_radius
    
    elif R > car.r_1 and R < car.r_2:
        numerator1 = ((9549.3*car.gear_reduction*car.p_max) / car.r_2) - (car.gear_reduction*car.t_max)
        result = (numerator1 / (car.r_2 - car.r_1))*((R-car.r_1)/car.tire_radius)+((car.gear_reduction*car.t_max)/car.tire_radius)

    elif R >= car.r_2:
        result = (9549.3*car.gear_reduction*car.p_max) / (car.tire_radius * R)
    
    return result

def H_of_v(v,car):

    minimum1 = car.static_friction*car.mass*car.gravitational_acceleration
    R = find_R(v,car)
    minimum2 = f_m_of_R(R,car)

    if minimum1 < minimum2:
        minimum = minimum1
    else:
        minimum = minimum2
    
    in_parentheses = minimum - (0.5)*car.air_density*car.drag_coefficient*car.surface_area*(v**2)
    result = (1/car.mass)*(in_parentheses)

    return result

