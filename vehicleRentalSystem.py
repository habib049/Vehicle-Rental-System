
# this class is layer above the reservation class making our work easy
# It handles all the reservations by handling the data of reservation class
# means reservation is a single reservation where Reservations class holds dict of reservations
class Reservations:
    def __init__(self):
        # for storing the reservation with credit card number as a key
        self.__reservations = dict()

    def is_reserved(self, vin):
        # check if present in reservations return true else false
        if vin in self.__reservations:
            return True
        else:
            return False

    def get_vin_for_reservation(self, credit_card):
        # getting cin against the credit card number
        return self.__reservations[credit_card].get_vin()

    def add_reservation(self, reservation):
        # after the credit card number I put reservation dict against the credit card number
        self.__reservations[reservation.get_credit_card()] = reservation

    def find_reservation(self, credit_card):
        # check if present in reservations return true else false
        if credit_card in self.__reservations:
            return True
        else:
            return False

    def cancel_reservation(self, credit_card):
        # del is used in pyhton to delete the object
        del (self.__reservations[credit_card])


class Reservation:
    def __init__(self, name, address, credit_card, vin):
        # __ variables are private indirectly
        self.__name = name
        self.__address = address
        self.__credit_card = credit_card
        self.__vin = vin

    # these functions are provinding data for specific reservation
    def get_name(self):
        return self.__name

    def get__address(self):
        return self.__address

    def get_credit_card(self):
        return self.__credit_card

    def get_vin(self):
        return self.__vin


# this class is same as Vehicles act as a layer over vehicle cost class
# it also act the same and handle multiple costs ata single time by holding multiple
# objects of vehicleCost class
class VehicleCosts:
    def __init__(self):
        # in dict it is easy to maintain the records of costs in key value pair
        self.__costs = dict()
        # opening a file and reading a data from file
        with open("RentalCost.txt") as file:
            lines = file.readlines()  # it read all lines in the file
            self.__costs["car"] = VehicleCost(lines[0],
                                              lines[1])  # first two line in file contains car daily and weekly rates
            self.__costs["van"] = VehicleCost(lines[2], lines[3])  # next two for vans
            self.__costs["truck"] = VehicleCost(lines[4], lines[5])  # next two for trucks

    def get_vehicle_cost(self, vehicle_type):
        # first check whether vehicle type exists or not
        if vehicle_type in self.__costs.keys():
            return [self.__costs[vehicle_type].get_daily_rate(), self.__costs[vehicle_type].get_weekly_rate()]
        return None  # if not present it simply return none instead of error

    def calculate_rent_cost(self, vehicle_type, rental_period, rental_days):
        # first collecting the cost of vehicle

        vehicle_cost = self.get_vehicle_cost(vehicle_type)
        rent_rate = ""

        if rental_period == 1:  # 1 means it is daily
            rent_rate = vehicle_cost[0]  # at zero index day cost is places
        elif rental_period == 2:  # 2 means it is weekly
            rent_rate = vehicle_cost[1]  # at 1 index weeekly cost is palced

        basic_rent = int(rental_days) * rent_rate

        # now all the data goes in the form of list
        return basic_rent


# this class helps us by providing access to all kind of rental cost separately
# so that it is easily call any rent at any point of the program
class VehicleCost:
    def __init__(self, daily_rate, week_rate):
        # print(daily_rate,week_rate,weekend_rate,free_miles,charge_per_mile,insurance_rate)
        # double underscore means variable are private indirectly
        # converting to flaot so that we can perform calculations on it
        self.__daily_rate = float(daily_rate)
        self.__week_rate = float(week_rate)

    # these function provide details of single costs object

    def get_daily_rate(self):
        return self.__daily_rate

    def get_weekly_rate(self):
        return self.__week_rate

    def get_costs(self):
        # returning the list of costs of all types
        return [self.__daily_rate, self.__week_rate]


# this class is made for making a layer over vehicles
# so that we can easily maintain our data of vehicles
# it hold the list of vehicles in this class

class Vehicles:
    def __init__(self):
        # this is private list of all vehicles
        self.__vehicles = list()  # list() is the constructor of list
        # this counter is used to separate the data of different vehicles
        self.__counter = 0
        # reading a data form file
        # with is the context menu it automatically cover up all the objects after ending it like closing file etc
        with open("VehiclesStock.txt") as file:
            lines = file.readlines()  # it read all lines in the file
            for line in lines:
                if '_' in line:  # this is used to separate the data fo different vehicles
                    self.__counter += 1
                    continue
                if self.__counter == 0:
                    # split function is used to spilt the string into array on the basis of given character
                    lines = line.split("|")
                    # making a car object and storing it in the cars list
                    car = Car(lines[0], lines[1], lines[2], lines[3], lines[4].strip('\n'))
                    self.__vehicles.append(car)
                    # .strip('\n') function is used to cut out the '\n' from the end of string

                elif self.__counter == 1:
                    lines = line.split("|")
                    # making a van object and storing it in the vans list
                    van = Van(lines[0], lines[1], lines[2], lines[3].strip('\n'))
                    self.__vehicles.append(van)
                    # .strip('\n') function is used to cut out the '\n' from the end of string

                elif self.__counter == 2:
                    lines = line.split("|")
                    # making a van object and storing it in the vans list
                    truck = Truck(lines[0], lines[1], lines[2], lines[3].strip('\n'))
                    self.__vehicles.append(truck)
                    # .strip('\n') function is used to cut out the '\n' from the end of string

    def get_vehicle(self, vin):
        # iterating over through the vehicles and check the vin number one by one
        i = 0
        while True:
            if self.__vehicles[i].get_vin() == vin:
                return self.__vehicles[i]
            i += 1

    def add_vehicle(self, vehicle):
        # vehicle object is passed we simply put it in our list
        self.__vehicles.append(vehicle)

    def num_avail_vehicle(self, vehicle_type):
        # we simply use our own function getting particular types of vehicles and find its length using len
        return len(self.get_avail_vehicle(vehicle_type))

    def get_avail_vehicle(self, vehicle_type):
        # we have to create of list of all available vehicles of specific type
        available_vehicles = list()
        for veh in self.__vehicles:
            if veh.get_type() == vehicle_type:
                if veh.is_reserved() == 0:  # means the value of reserved is 0 and vehicle is available
                    available_vehicles.append(veh)
        return available_vehicles

    def get_vehicle_types(self):
        return ['Car', 'Van', 'Truck']

    # make vehicle un reserve
    def unreserve_vehicle(self, vin):
        # first we have to find that particular vehicle
        i = 0
        while True:
            if self.__vehicles[i].get_vin() == vin:
                self.__vehicles[i].set_reserved(0)
                break
            i += 1


# vehicle class

class Vehicle:
    def __init__(self, miles_per_gallons, vin):
        # double underscore means variable are private indirectly
        self.__is_reserved = 0  # for every vehicle initial reservation status is none means 0
        self.__miles_per_gallons = miles_per_gallons
        self.__vin = vin

    def get_type(self):
        return self.__class__.__name__  # we get the our class first then is name (dunder methods)

    def get_vin(self):
        return self.__vin

    def get_description(self):
        # making a description and returning it
        return '\tMiles per gallon : ' + self.__miles_per_gallons + '\tVIN : ' + self.__vin

    def is_reserved(self):
        return self.__is_reserved

    def set_reserved(self, reserved_value):
        self.__is_reserved = reserved_value


# Car class
class Car(Vehicle):
    def __init__(self, vin, car_model, miles_per_gallons, pasengers, num_of_doors):
        # calling its parent constructor and setting its data in its parent class
        super().__init__(miles_per_gallons, vin)
        # double underscore means variable are private indirectly
        self.__passengers = pasengers
        self.__num_of_doors = num_of_doors
        self.__car_model = car_model

    def get_description(self):
        # making a description and returning it
        return self.__car_model + '\t\tpassenger :' + self.__passengers + '\tdoors : ' + self.__num_of_doors \
               + super(Car, self).get_description()  # getting the description from its parent also
        # super refers to the parent class


# Van Class
class Van(Vehicle):
    def __init__(self, vin, van_name, miles_per_gallon, passengers):
        # calling its parent constructor and setting its data in its parent class
        super().__init__(miles_per_gallon, vin)
        self.__passengers = passengers
        self.__van_name = van_name

    def get_description(self):
        # making a description and returning it
        return self.__van_name + '\t\tpassenger : ' + self.__passengers \
               + super(Van, self).get_description()  # getting the description from its parent also
    # super refers to the parent class


# truck class
class Truck(Vehicle):
    def __init__(self, vin, miles_per_gallon, length, num_of_rooms):
        super().__init__(miles_per_gallon, vin)
        # double underscore means variable are private indirectly
        # reference Dunder methods
        self.__length = length
        self.__num_of_room = num_of_rooms

    def get_description(self):
        # making a description and returning it
        return self.__length + ' feet    Rooms: ' + self.__num_of_room \
               + super(Truck, self).get_description()  # getting the description from its parent also
    # super refers to the parent class


# s=Startup()
# s.start()




def start_function():
    vehicles_costs = VehicleCosts()
    vehicles = Vehicles()
    reservations = Reservations()

    # printing welcome
    print('*******************************************************************')
    print('           * Welcome to friendly vehicle rental agency *           ')
    print('********************************************************************')

    # getting input and showing menu
    while True:
        # printing menu
        print('\n\n')
        print("  <<<< Main Menu >>>")
        print('1- Display vehicles types')
        print('2- Check rental costs')
        print('3- Display available vehicles')
        print('4- Get cost of specific rental')
        print('5- Make reservation')
        print('6- Cancel reservation')
        print('7- Quit\n')

        # int conversion . so that it is easily comparable

        # getting input

        input_valid = False

        selected_option = input("Enter your choice : ")
        while not input_valid:
            # check if it digit or not
            if selected_option.isdigit():
                # check if is in range of option or not
                if 1 > int(selected_option) < 7:
                    selected_option = input("Enter your choice : ")
                else:
                    # valid input break the loop and return the value
                    selected_option = int(selected_option)  # converting to int
                    input_valid = True
            else:
                selected_option = input("Enter your choice : ")

        # checking number and calling respective functions
        if selected_option == 1:

            print('***************** Types of vehicles available for rent *******************')
            vehs = vehicles.get_vehicle_types()
            # using enumerate er get both index and value of that index
            for index, value in enumerate(vehs):
                print(index + 1, " - " + value)
            print('****************************************************************************')

        elif selected_option == 2:

            print("1- Car")
            print("2- Van")
            print("3- Truck")
            # int conversion . so that it is easily comparable
            option = int(input("Enter type of vehicle : "))

            if option == 1:
                print('************************* Rental costs for cars ******************************\n')
                print("Daily\t\t\tweekly")
                charges = vehicles_costs.get_vehicle_cost("car")  # getting car costs
                # only strings are concatenable so every variable is converted into string
                print(str(charges[0]) + "\t\t\t" + str(charges[1]))
                print('\n*******************************************************************************')

            elif option == 2:
                print('************************** Rental costs for vans ********************************\n')
                print("Daily\tweekly")
                charges = vehicles_costs.get_vehicle_cost("van")  # getting van costs
                # only strings are concatenable so every variable is converted into string
                print(str(charges[0]) + "\t" + str(charges[1]))
                print('\n*********************************************************************************')

            elif option == 3:
                print('******************************* Rental costs for trucks *****************************\n')
                print("Daily\tweekly")
                charges = vehicles_costs.get_vehicle_cost("truck")  # getting trucks costs
                # only strings are concatenable so every variable is converted into string
                print(str(charges[0]) + "\t" + str(charges[1]))
                print('\n*************************************************************************************')

        elif selected_option == 3:

            print("1- Car")
            print("2- Van")
            print("3- Truck")
            # int conversion . so that it is easily comparable
            option = int(input("Enter type of vehicle : "))

            if option == 1:
                available_vehicles = vehicles.get_avail_vehicle(
                    "Car")  # getting available vehicles of type car
                print('************************************* Available cars *********************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n***************************************************************************************')

            elif option == 2:
                available_vehicles = vehicles.get_avail_vehicle(
                    "Van")  # getting available vehicles of type van
                print('*********************************** Available vans *******************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n***********************************************************************************')

            elif option == 3:
                available_vehicles = vehicles.get_avail_vehicle(
                    "Truck")  # getting available vehicles of type truck
                print('******************************** Available trucks *****************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n********************************************************************************')

        elif selected_option == 4:
            print("1- Car")
            print("2- Van")
            print("3- Truck")
            # int conversion . so that it is easily comparable
            option = int(input("Enter type of vehicle : "))

            print("1 - daily\t2 - Weekly")
            rental_period = int(input("Enter rental period : "))
            # collecting other data
            rental_time = input("How many days you need the vehicle : ")
            number_of_miles = input("Number of miles except to drive : ")

            if option == 1:
                print('\n\n************************ Estimated car rental cost ***********************')
                # getting rental cost
                cost = vehicles_costs.calculate_rent_cost('car', rental_period, rental_time)
                if rental_period == 1:
                    print("Daily rental for " + str(rental_time) + " days would be $", str(cost))
                elif rental_period == 2:
                    print("Weekly rental for " + str(rental_time) + " weeks would be $", str(cost))
                print("Your total for " + str(rental_time) + " would be " + str(cost * int(rental_time)))
                print('*******************************************************************************')

            elif option == 2:
                print('\n\n************************ Estimated van rental cost ***********************')
                # getting rental cost
                cost = vehicles_costs.calculate_rent_cost('van', rental_period, rental_time)
                if rental_period == 1:
                    print("Daily rental for " + str(rental_time) + " days would be $", str(cost))
                elif rental_period == 2:
                    print("Weekly rental for " + str(rental_time) + " weeks would be $", str(cost))
                print("Your total for " + str(rental_time) + " would be " + str(cost * int(rental_time)))
                print('*******************************************************************************')

            elif option == 3:
                print('\n\n************************ Estimated truck rental cost ***********************')
                # getting rental cost
                cost = vehicles_costs.calculate_rent_cost('truck', rental_period, rental_time)
                if rental_period == 1:
                    print("Daily rental for " + str(rental_time) + " days would be $", str(cost))
                elif rental_period == 2:
                    print("Weekly rental for " + str(rental_time) + " weeks would be $", str(cost))
                print("Your total for " + str(rental_time) + " would be " + str(cost * int(rental_time)))
                print('*******************************************************************************')

        elif selected_option == 5:

            # variables to get record
            name = ""
            address = ""
            credit_card_number = ""
            vin = ""
            print("1- Car")
            print("2- Van")
            print("3- Truck")
            # int conversion . so that it is easily comparable
            option = int(input("Enter type of vehicle : "))

            if option == 1:
                available_vehicles = vehicles.get_avail_vehicle("Car")
                print('************************************* Available cars *********************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n***************************************************************************************')
                vehicle_number = input("Enter a number of vehicle to reserve : ")
                print(available_vehicles[int(vehicle_number) - 1].get_description())

                vin = vehicles.get_avail_vehicle("Car")[int(vehicle_number) - 1].get_vin()

                name = input("Enter first name and last name : ")
                address = input("Enter address : ")
                credit_card_number = input("Enter credit card number : ")
                # making a new object of reservation and store it in reservations
                reservation = Reservation(name, address, credit_card_number, vin)
                # making the vehicle reserved
                vehicles.get_vehicle(vin).set_reserved(1)
                reservations.add_reservation(reservation)
                print(" * reservation made * ")

            elif option == 2:
                available_vehicles = vehicles.get_avail_vehicle("Van")
                print('*********************************** Available vans *******************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n***********************************************************************************')
                vehicle_number = input("Enter a number of vehicle to reserve : ")
                print(available_vehicles[int(vehicle_number) - 1].get_description())  # getting vehicle description

                vin = vehicles.get_avail_vehicle("Van")[int(vehicle_number) - 1].get_vin()

                name = input("Enter first name and last name : ")
                address = input("Enter address : ")
                credit_card_number = input("Enter credit card number : ")
                # making a new object of reservation and store it in reservations
                reservation = Reservation(name, address, credit_card_number, vin)
                # making the vehicle reserved

                vehicles.get_vehicle(vin).set_reserved(1)
                print("Value of set reserve is ", vehicles.get_vehicle(vin).is_reserved())
                reservations.add_reservation(reservation)
                print(" * reservation made * ")

            elif option == 3:
                available_vehicles = vehicles.get_avail_vehicle("Truck")
                print('******************************** Available trucks *****************************\n')
                for index, value in enumerate(available_vehicles):
                    print(str(index + 1) + "- " + value.get_description())  # getting description
                print('\n********************************************************************************')
                vehicle_number = input("Enter a number of vehicle to reserve : ")
                print(available_vehicles[int(vehicle_number) - 1].get_description())

                vin = vehicles.get_avail_vehicle("Truck")[int(vehicle_number) - 1].get_vin()

                name = input("Enter first name and last name : ")
                address = input("Enter address : ")
                credit_card_number = input("Enter credit card number : ")
                # making a new object of reservation and store it in reservations
                reservation = Reservation(name, address, credit_card_number, vin)
                # making the vehicle reserved
                vehicles.get_vehicle(vin).set_reserved(1)

                reservations.add_reservation(reservation)
                print(" * reservation made * ")

        elif selected_option == 6:

            credit_card_number = input("Enter your credit card number : ")
            if reservations.find_reservation(credit_card_number):  # first check if we have reservation against this credit card number
               vin = reservations.get_vin_for_reservation(credit_card_number)
                # making the vehicle unreserve
               vehicles.unreserve_vehicle(vin)
               reservations.cancel_reservation(credit_card_number)  # cancel the reservation
               print(" ** Reservation canceled **")
            else:
                print("** Reservation not found **")

        else:  # if user selects 7 the program exists
            break


start_function()