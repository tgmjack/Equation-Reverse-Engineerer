import copy
import random
import numpy
import pandas as pd
import time

##############################################
############## wtf only doing first bracket?    # search in comment 
############## overflow evveror
############## overflow eerror somehow gets stuck forever
############## investigate 10-6 mses seems sus
############## investigate what happens if i actually give it v=u+at
############## need to add chunks on
#
############ because of this crap am i missing last ting from or does eq even maake sense 
#full_bracket_operation += "(("+str(weight)+ " * "  + str(var_nam)+" ** " +str(power) + ") + " + str(bias) + " ) "
#                if count != number_of_terms-1:
#                    full_bracket_operation += the_operation
#
# pass in v = u + at to see  rmse
#
###############################################




#####    ensure every single index is more accurate each time, then for the ones that were all correct for bestr rmse


max_brackets_per_neuron = 6
max_bracket_terms = 4
base_layer_pop = 10
subsequent_layer_pop = 200

variables = ["s","u","v" , "a" , "t" ]

ss = [10, 3 , 2.4 , 19.03842 ,0.5 , 1 , 3 , 9 , 15 , 10005, 1100.899946]
us = [1 , 9 , -3 , 1 , 90 , 2 , 2 , 8 , 60 , -82499.333 , 1100899.94]
vs = [0 , 3 , 9 , 0.1 , 1 , 3 , 1 , 7 , 80 , 82500.67 , 1100899.952]
a_s = [-0.05 , -12 , 15 , -0.026 , -8099 , 2.5 , -0.5 , -0.833 , 93.33 , 11 , 12]
ts = [20 , 0.5 , 0.8 , 34.615, 0.010989 , 0.4 , 2 , 1.2 , 0.2142, 15000 , 0.001]

all_data = [ss , us , vs , a_s , ts]
all_data = {'s':ss, 'u':us, 'v':vs, 'a':a_s, 't':ts}

#new_s= 11009
#new_a = 12.replace('"','').replace("'","")
#new_t = 0.01
#u = (new_s - (0.5 *new_a * (new_t ** 2)))/ new_t

#print(u)
#print(9/0)

s = 11009
u = 1100899.94
a = 12
t = 0.01
v = u + (a * t)
print(v)
min_error = 0.1
for s, u , v , a , t , count in zip(ss,us,vs, a_s, ts, range(len(ts)) ):
    print(str(count)+ "  count  ")
    if abs(v - (u + (a*t))) < min_error:
        pass
    else:
        print(v)
        print(u + (a*t))
        print(1/0)
    if abs(s - ((u*t)+ ((0.5)*(a * (t**2))))) < min_error:
        pass
    else:
        print(s)
        print((u*t)+ ((0.5)*(a * (t**2))))
        print(2/0)

    if abs(v - ((((u**2)+ (2 * a * s ))**0.5))) < min_error:
        pass
    else:
        print(v)
        print((u**2)+ (2 * a * s)**0.5)
        print(3/0)

variable_to_calculate = "t"



#    print(9/0)



def choose_equation_chunk(index):
    this_bracket= {"weights":[], "biases":[] , "variables":[] , "variable_names":[] , "indices":[] , "function":[] , "full_bracket_operation":[] }
    number_of_terms = random.randint( 1 , max_bracket_terms)
    full_bracket_operation = ""
    for count in range(number_of_terms):
        weight = random.random()
        this_bracket["weights"].append(weight)
        bias = random.random()
        if bias<0.5:
            bias = 0
        else:
            bias = random.random()
        this_bracket["biases"].append(bias)
        var_nam = variable_to_calculate
        while (var_nam == variable_to_calculate):
            var_chooser = random.randint(0, len(variables)-1)
            var_nam = variables[var_chooser]

        var = all_data[var_nam][index]
        this_bracket["variables"].append(var)
        this_bracket["variable_names"].append(var_nam)
        power = random.random()

        if power < 0.3:
            power = 1
        elif power < 0.6:
            power = 2
        elif power < 0.9:
            power = 3
        else:
            power = random.random()

        this_bracket["indices"].append(power)
        operation_chooser = random.random()
        if operation_chooser < 1:
            the_operation = "+"
        if operation_chooser < 0.75:
            the_operation = "*"
        if operation_chooser < 0.5:
            the_operation = "-"
        if operation_chooser < 0.25:
            the_operation = "/"
        this_bracket['function'].append(the_operation)

        full_bracket_operation += "(("+str(weight)+ " * "  + str(var_nam)+" ** " +str(power) + ") + " + str(bias) + " ) "
        if count != number_of_terms-1:
            full_bracket_operation += the_operation
    this_bracket['full_bracket_operation'] = full_bracket_operation;
    return this_bracket


def update_equation_chunks(previous_best_chunks , prev_bracket_ops , index):
    og_chunks = previous_best_chunks
    copy = previous_best_chunks
    chance_to_change_a_bit = 0.5
    for bracket in range(len(previous_best_chunks)):  ######
        for chunk in range(len(previous_best_chunks[bracket]["weights"])):
            change_at_all_chooser = random.random()
            if change_at_all_chooser < chance_to_change_a_bit:
                weights_chooser = random.random()
                if weights_chooser < 0.2:
                    copy[bracket]["weights"][chunk] = copy[bracket]["weights"][chunk] + random.random()
                elif weights_chooser < 0.4:
                    copy[bracket]["weights"][chunk] = copy[bracket]["weights"][chunk] - random.random()
                elif weights_chooser < 0.6:
                    copy[bracket]["weights"][chunk] = 0
                elif weights_chooser < 0.95:
                    copy[bracket]["weights"][chunk] = 1
                else:
                    copy[bracket]["weights"][chunk] += 1


            change_at_all_chooser = random.random()
            if change_at_all_chooser < chance_to_change_a_bit:
                biases_chooser = random.random()
                if biases_chooser < 0.1:
                    copy[bracket]["biases"][chunk] += random.random()
                elif biases_chooser < 0.2:
                    copy[bracket]["biases"][chunk] -= random.random()
                elif biases_chooser < 0.3:
                    copy[bracket]["biases"][chunk] += 1
                elif biases_chooser < 0.4:
                    copy[bracket]["biases"][chunk] -= 1
                elif biases_chooser < 0.65:
                    copy[bracket]["biases"][chunk] = 1
                else:
                    copy[bracket]["biases"][chunk] = 0

            change_at_all_chooser = random.random()
            if change_at_all_chooser < chance_to_change_a_bit:
                powers_chooser = random.random()
                if powers_chooser < 0.1:
                    copy[bracket]["indices"][chunk] += random.random()
                elif powers_chooser < 0.2:
                    copy[bracket]["indices"][chunk] -= random.random()
                elif powers_chooser < 0.4:
                    copy[bracket]["indices"][chunk] = 2
                elif powers_chooser < 0.6:
                    copy[bracket]["indices"][chunk] = 3
                elif powers_chooser < 0.7:
                    copy[bracket]["indices"][chunk] = 0.5
                else:
                    copy[bracket]["indices"][chunk] = 1

       #     invert_chooser = random.random()
        #    if invert_chooser < 0.3:
         #       if invert_chooser < 0.05:
          #          a["variable_names"][aa] = " ( 1 / "+ str(a["variable_names"][aa]) + " ) "
           #         a["variables"][aa] = 1 / 2+ a["variables"][aa]


             #       self.this_neurons_operation_despription += "        ...         ( " + this_bracket["full_bracket_operation"] + " )      ...        " + str(this_bracket_operation)
   # print(previous_best_chunks)


#    print("start deciding what to remove ")
    new_description = ""
    index_to_remove = []
    for a , brak_op , brak_counter in zip(previous_best_chunks , prev_bracket_ops , range(len(previous_best_chunks)) ): ## re describe operation
#        print("new brak")
        full_bracket_operation = ""
        for aa in range(len(a["biases"])):
            ###### decide whether to add or take away whole terms
  #          print("  t  ")
            keep_this_term = True
            terms_chooser = random.random() # 10% to remove term
            if terms_chooser < 0.05:
   #             print("removing ")
                keep_this_term = False


            if keep_this_term:
                w = str(a["weights"][aa])
                full_bracket_operation += "(("+w+ " * "  + str(a["variable_names"][aa])+" ** " +str(a["indices"][aa]) + ") + " + str(a["biases"][aa]) + " ) "
          #      if aa != len(a["biases"])-1:
    #            print(w+ " * "  + str(a["variable_names"][aa])+" ** " +str(a["indices"][aa]) + ") + " + str(a["biases"][aa]) + " ) "+ "   =     werre including this ")
                full_bracket_operation += str(a["function"][aa])
            else:
                index_to_remove.append([brak_counter , aa])
                w = str(a["weights"][aa])
     #           print("not putting this in      =      (("+w+ " * "  + str(a["variable_names"][aa])+" ** " +str(a["indices"][aa]) + ") + " + str(a["biases"][aa]) + " ) ")
        new_description += full_bracket_operation + "  " + brak_op
        
 #   print("done deciding what to remove")
  #  print(" bite ")
   # print(previous_best_chunks)
  #  print(" bite ")

    index_to_remove.reverse()
    for t in index_to_remove:
#        print(t[0])
 #       print(t[1])
  #      print("#####")
   #     print(previous_best_chunks[t[0]])

        og = previous_best_chunks[t[0]]["weights"]
   #     print("-----------------------")
    #    print(og)
     #   print(t[1])
        del og[t[1]]
        previous_best_chunks[t[0]]["weights"] = og
        #########################################
        og = previous_best_chunks[t[0]]["biases"]
        del(og[t[1]])
        previous_best_chunks[t[0]]["biases"] = og
        #########################################
        og = previous_best_chunks[t[0]]["indices"]
        del(og[t[1]])
        previous_best_chunks[t[0]]["indices"] = og
        ##########################################
        og = previous_best_chunks[t[0]]["variable_names"]
        del(og[t[1]])
        previous_best_chunks[t[0]]["variable_names"] = og
        ##########################################
        og = previous_best_chunks[t[0]]["variables"]
        del(og[t[1]])
        previous_best_chunks[t[0]]["variables"] = og
        ##########################################
        og = previous_best_chunks[t[0]]["function"]
        del(og[t[1]])
        previous_best_chunks[t[0]]["function"] = og

#    previous_best_chunks.pop()
 #   print(w)   #   print(" whats left is below  ")    #     print(copy)
  #  print("======================")
   # print(previous_best_chunks)
  #  print(69/0)

########
##       adding new chunks to brackets bellow
########
    full_bracket_operation = ""
    for bracket in range(len(previous_best_chunks)):  ######
   #     print("y")
        full_bracket_operation +=  " aaaaaaa ( "
        for chunk in range(len(previous_best_chunks[bracket]["weights"])):
#            print(" bracket "+str(bracket) + "    ,   chunk "+str(chunk))
            new_thing_here_chooser = random.random()
            if new_thing_here_chooser < 0.05:
                
 #               print("added new terms ")

                weight = random.random()
                previous_best_chunks[bracket]["weights"].insert(chunk, weight)
                bias = random.random()
                if bias<0.5:
                    bias = 0
                else:
                    bias = random.random()
            #    this_bracket["biases"].append(bias)
                previous_best_chunks[bracket]["biases"].insert(chunk, bias)
                var_nam = variable_to_calculate
                while (var_nam == variable_to_calculate):
                    var_chooser = random.randint(0, len(variables)-1)
                    var_nam = variables[var_chooser]

                var = all_data[var_nam][index]
              #  this_bracket["variables"].append(var)
                previous_best_chunks[bracket]["variables"].insert(chunk, var)
                previous_best_chunks[bracket]["variable_names"].insert(chunk, var_nam)
#                this_bracket["variable_names"].append(var_nam)
                power = random.random()

                if power < 0.3:
                    power = 1
                elif power < 0.6:
                    power = 2
                elif power < 0.9:
                    power = 3
                else:
                    power = random.random()

               # this_bracket["indices"].append(power)

                previous_best_chunks[bracket]["indices"].insert(chunk, power)
                operation_chooser = random.random()
                if operation_chooser < 1:
                    the_operation = "+"
                if operation_chooser < 0.75:
                    the_operation = "*"
                if operation_chooser < 0.5:
                    the_operation = "-"
                if operation_chooser < 0.25:
                    the_operation = "/"
                previous_best_chunks[bracket]["function"].insert(chunk, the_operation)
        #        this_bracket['function'].append(the_operation)

       #         full_bracket_operation += "(("+str(weight)+ " * "  + str(var_nam)+" ** " +str(power) + ") + " + str(bias) + " ) "
        #        if count != number_of_terms-1:
         #           full_bracket_operation += the_operation



                full_bracket_operation += "(("+str(weight)+ " * "  + str(var_nam)+" ** " +str(power) + ") + " + str(bias) + " ) "
            # chunk in range(len(previous_best_chunks[bracket]["weights"])
                if count != len(previous_best_chunks[bracket]["weights"])-1:
                    full_bracket_operation +=  " ) "+str(the_operation)
                    copy[bracket]["weights"][chunk] = copy[bracket]["weights"][chunk] + random.random()

########
##       adding new brackets to neuron bellow
########

    full_bracket_operation = ""
    for bracket in range(len(previous_best_chunks)):  ######
  #      print("y")
        full_bracket_operation +=  "  (   "
        for chunk in range(len(previous_best_chunks[bracket]["weights"])):
  #          print(" bracket "+str(bracket) + "    ,   chunk "+str(chunk))
            weight = previous_best_chunks[bracket]["weights"][chunk]
            var_nam = previous_best_chunks[bracket]["variable_names"][chunk]
            power = previous_best_chunks[bracket]["indices"][chunk]
            bias  = previous_best_chunks[bracket]["biases"][chunk]
            op = previous_best_chunks[bracket]["function"][chunk]
            full_bracket_operation += "(("+str(weight)+ " * "  + str(var_nam)+" ** " +str(power) + ") + " + str(bias) + " ) "
            if chunk != len(previous_best_chunks[bracket]["weights"])-1:
                full_bracket_operation += str(op)
            # chunk in range(len(previous_best_chunks[bracket]["weights"])
 
        full_bracket_operation +=  "  )  "
        if bracket != len(previous_best_chunks) -1 :
            full_bracket_operation += "  "+ str(prev_bracket_ops[bracket])
        #   +str(the_operation)
                
    return previous_best_chunks, full_bracket_operation

class neuron:
    def __init__(self ,  first , previous_best_neuron = 0):#
   #     print("meking new neuron 66666666666666666666666666666666666666666")
        if first:
            self.equation_chunks = []
            self.bracket_operations = []
            self.number_of_bracketed_areas = random.randint( 1 , max_brackets_per_neuron)
            self.neurons_index = random.randint( 0  , len(variables) )
            self.this_neurons_operation_despription = ""
            for count in range(self.number_of_bracketed_areas):
                this_bracket = choose_equation_chunk(self.neurons_index)
                if count == self.number_of_bracketed_areas -1:
                    this_bracket_operation = "done"
                else:
                    operation_chooser = random.random()
                    if operation_chooser < 1:
                        this_bracket_operation = "+"
                    if operation_chooser < 0.75:
                        this_bracket_operation = "*"
                    if operation_chooser < 0.5:
                        this_bracket_operation = "-"
                    if operation_chooser < 0.25:
                        this_bracket_operation = "/"
                self.equation_chunks.append(this_bracket)
                self.bracket_operations.append(this_bracket_operation)
                self.this_neurons_operation_despription += "        ...         ( " + this_bracket["full_bracket_operation"] + " )      ...        " + str(this_bracket_operation)
            self.output = "not set";

    #def __init__(self , previous_best_neuron):
        else:
            self.equation_chunks = []
            self.bracket_operations = previous_best_neuron.bracket_operations
            self.number_of_bracketed_areas = previous_best_neuron.number_of_bracketed_areas
            self.neurons_index = previous_best_neuron.neurons_index
            self.this_neurons_operation_despription = ""
#            print("bef below")
 #           print(previous_best_neuron.this_neurons_operation_despription)
  #          print("bef above")
            self.equation_chunks , self.this_neurons_operation_despription = update_equation_chunks(previous_best_neuron.equation_chunks  ,  previous_best_neuron.bracket_operations , self.neurons_index)
   #         print("aft below")
    #        print(self.this_neurons_operation_despription)
     #       print("aft above")
#           #             #           #   print(9/0)
            self.output = "not set";

    def bracket_values(self):
        bracket_totals = []
        for bracket in self.equation_chunks:
            bracket_total = 0
            for index in range(len(bracket["weights"])):
                early_fail = False
                try:
                    this_term = (bracket["weights"][index]*(bracket["variables"][index]** bracket["indices"][index] )+ bracket["biases"][index])
                except ZeroDivisionError:
                    early_fail =True
                    bracket_total = "zero div error"
                if not early_fail:
                    if (not  isinstance(this_term, complex)) & (type(bracket_total) != str):
                        if index == 0:
                            bracket_total = bracket_total + this_term
                        elif (bracket["function"][index-1] == "+"):
                            bracket_total = bracket_total + this_term
                        elif (bracket["function"][index-1] == "*"):
                            bracket_total = bracket_total * this_term
                        elif (bracket["function"][index-1] == "-"):
                            bracket_total = bracket_total - this_term
                        elif (bracket["function"][index-1] == "/"):
                            try:
                                bracket_total = bracket_total / this_term
                            except:
                                bracket_total = "div by zero"
                    else:
                        bracket_total = "zero div error"
                bracket_totals.append(bracket_total)
        simpler_output = ""
        for op, tot in zip(self.bracket_operations , bracket_totals):
            simpler_output+= str(tot)
            if "done" not in op:
                simpler_output+= str(op)
        return simpler_output;
##################################################
    def forward(self):
        terms_holder = []
        bracket_totals = []
 #       print("============     new forard attempt")
        for bracket in self.equation_chunks:
            bracket_total = 0
            for index in range(len(bracket["weights"])):
                early_fail = False
                try:
                    this_term = (bracket["weights"][index]*(bracket["variables"][index]** bracket["indices"][index] )+ bracket["biases"][index])
                except ZeroDivisionError:
                    early_fail =True
                    bracket_total = "zero div error"
                if not early_fail:
                    if (not  isinstance(this_term, complex)) & (type(bracket_total) != str):
                        terms_holder.append(this_term)
                        terms_holder.append(bracket["function"][index])
                        if index == 0:
        #                    print(this_term)
      #                      print("ak 1")
                            bracket_total = bracket_total + this_term
                        elif (bracket["function"][index-1] == "+"):
       #                     print("ak 2")
                            bracket_total = bracket_total + this_term
                        elif (bracket["function"][index-1] == "*"):
        #                    print("ak 3")
                            bracket_total = bracket_total * this_term
                        elif (bracket["function"][index-1] == "-"):
         #                   print("ak 4")
                            bracket_total = bracket_total - this_term

                        elif (bracket["function"][index-1] == "/"):
                            try:
          #                      print("ak 5")
                                bracket_total = bracket_total / this_term
                            except:
                              #  print(this_term)
                             #   print(bracket_total)
           #                     print("ak 6")
                                bracket_total = "div by zero"
                    else:
                        bracket_total = "zero div error"
           #     print(bracket_total)
            #    print(bracket_totals)
             #   print("  888888888888   ")
                bracket_totals.append(bracket_total)
        #        print(bracket_total)
         #       print(bracket_totals)
   #     print("===============     bracket totals below")
    #    for b in bracket_totals:
     #       print(b)
      #  print("===============     bracket totals above")
        full_output = 0
        for bracket_total, op , bracket_counter in zip(bracket_totals, self.bracket_operations , range(len(bracket_totals))):
       #     print(str(op) + " operation          total " + str(bracket_total))
            if bracket_total != "zero div error":
                if (not  isinstance(this_term, complex)) & ( type(bracket_total) != str )& ( type(full_output) != str or op == "done" ):
            #        print("ooooooookkkkkkkkkkkkkkkkk")
                    if bracket_counter == 0:                                   ############## wtf only doing first bracket?
                        if op == "+":
                            full_output += bracket_total
      #                      print("ok 1")
                        elif op == "-":
                            full_output -= bracket_total
       #                     print("ok 2")
                        elif op == "*":
                            full_output = full_output * bracket_total
        #                    print("ok 3")
                        elif op == "/":
                            try:
                                full_output =  full_output / bracket_total
         #                       print("ok 4")
                            except:
                                if full_output == 0:
                                    try:
                                        full_output =  1 / bracket_total
          #                              print("ok 5")
                                    except:
                   #                     print(full_output)
                  #                      print(bracket_total)
                              #  print(9/0)
                                        full_output =  "fail"
           #                             print("ok 6")
                        else:
                            if op == "done":
                                if bracket_counter == 0:
                                    full_output = bracket_total
                                pass
                            else:
                                print(9/0)
                    else:
                        if full_output == 0:
                            full_output = bracket_total
                else:
      #              print("ok fail")
                    full_output =  "fail"
       #             print(str(full_output) + "          current total of all brackets  ")
        #    print(str(full_output) + "       =   full output ")
            else:
      #              print("ok fail")
                full_output =  "fail"


        self.output = full_output

   #     print("===============     output   below")
    #     print(self.output)
     #     print("===============     output   above")
      #
       #
        #



    def forward_all_indexes(self):
        full_outputs = []
   #     for bracket in self.equation_chunks:
    #        print("bracket")
     #       print(bracket)
      #  print(9/0)

      #  print("===============================================")
        for all_other_indexs in range(len(us)):
            terms_holder = []
            bracket_totals = []

            for bracket in self.equation_chunks:
       #         print("bracket")
        #        print(bracket)
                bracket_total = 0
                for index in range(len(bracket["weights"])):
         #           print(bracket["variable_names"][index])  #  [all_other_indexs]
          #          print(all_data[bracket["variable_names"][index]][all_other_indexs])
                    if not (all_data[bracket["variable_names"][index]][all_other_indexs] == 0 and bracket["indices"][index] < 0):
                        if (not isinstance(bracket["indices"][index] , complex)):
                            try:
                                this_term = (bracket["weights"][index]*(all_data[bracket["variable_names"][index]][all_other_indexs]** bracket["indices"][index] )+ bracket["variables"][index])
                            except OverflowError:
                                this_term = "too big"
                                print("overflow evveror")
                            if this_term != "too big":
                                if (not  isinstance(this_term, complex)) & (type(bracket_total) != str):
                                    terms_holder.append(this_term)
                                    terms_holder.append(bracket["function"][index])

                                    if index == 0:
                                        #print(this_term)
                                        bracket_total = bracket_total + this_term
                                    elif (bracket["function"][index-1] == "+"):
                                        bracket_total = bracket_total + this_term
                                    elif (bracket["function"][index-1] == "*"):
                                        bracket_total = bracket_total * this_term
                                    elif (bracket["function"][index-1] == "-"):
                                        bracket_total = bracket_total - this_term

                                    elif (bracket["function"][index-1] == "/"):
                                        try:
                                            bracket_total = bracket_total / this_term
                                        except:
                                            bracket_total = "div by zero"
                   #             print(bracket_total)
                    #            print(bracket_totals)
                     #           print("  888888888888   ")

                            else:
                                this_term = "error "
                                bracket_total = "too big"
                        else:
                            this_term = "error "
                            bracket_total = "div by zero"
                    else:
                        this_term = "complex power error "
                        bracket_total = "complex power "
                    bracket_totals.append(bracket_total)





#######################################################
            full_output = 0
            for bracket_total, op , bracket_counter in zip(bracket_totals, self.bracket_operations , range(len(bracket_totals))):
           #     print(str(op) + " operation          total " + str(bracket_total))
                if (not  isinstance(this_term, complex)) & ( type(bracket_total) != str )& ( type(full_output) != str or op == "done" ):
            #        print("ooooooookkkkkkkkkkkkkkkkk")
                    if bracket_counter == 0:
                        if op == "+":
                            full_output += bracket_total
      #                      print("ok 1")        #           print("ok 1")
                        elif op == "-":
                            full_output -= bracket_total
       #                     print("ok 2")
                        elif op == "*":
                            full_output = full_output * bracket_total
        #                    print("ok 3")
                        elif op == "/":
                            try:
                                full_output =  full_output / bracket_total
         #                       print("ok 4")
                            except:
                                if full_output == 0:
                                    try:
                                        full_output =  1 / bracket_total
          #                              print("ok 5")
                                    except:
         #                               print(full_output)
        #                                print(bracket_total)
                              #  print(9/0)
 #                                       print(str(this_term)+ "          we had             " + str(bracket_total))
  #                                      print("div fail")
                                        full_output =  "fail"
           #                             print("ok 6")
                        else:
                            if op == "done":
                                if bracket_counter == 0:
                                    full_output = bracket_total
                                pass
                            else:
                                print(9/0)
                    else:
                        if full_output == 0:
                            full_output = bracket_total
                else:
      #              print("ok fail")
   #                 print(str(this_term)+ "          we had             " + str(bracket_total))
    #                print("complex n string thing")
                    full_output =  "fail"
    ###############################################
            full_outputs.append(full_output)


     #   print("returning ")
   #     print(full_outputs)
        return full_outputs


    def mean_squared_error(self):
  #      print("  ---------  ")
   #     print("bart to getr diffs")
        difs = self.forward_all_indexes()
    #    print(" GOT DIFS ")
        sum_error = 0
        diffs_that_counter = 0
        for d in range(len(difs)):
      #      print("    going through these diffs       = "+str(d))
            error = False
#            try:
            try:
                a = 1/ difs[d]
            except (ZeroDivisionError , TypeError):
       #         print(str(difs[d])+ " =             bad  difs[d] ")
                error = True;
            if not error:
                old_value = difs[d]
                propper_value = all_data[variable_to_calculate][d]
                dif = abs(old_value - propper_value);
        #        print(str(dif)+ "     this error ")
                sum_error += dif
         #       print(str(sum_error)+ "      total error so far ")
                diffs_that_counter+= 1

        if diffs_that_counter > 0:
            try:
                mse = (1/diffs_that_counter) * (sum_error ** 2)
            except OverflowError:
                print("overflow eerror ")
                mse = 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
          #  print("mse explanation below")
           # print(str(mse)+" =  ("+str(1/diffs_that_counter)+ ") * " + str(sum_error ** 2))
     #       time.sleep(19)
        else:
            mse = 9999999999999999999999999999999999999999999999999999999
     #   print(str(mse) + "    mse we got ")
        return mse

    def final_mean_squared_error(self):
       # print("  ---------  ")
        difs = self.forward_all_indexes()
        sum_error = 0
        working_dif_count = 0
        for d in range(len(difs)):
            try:
        #        print(difs[d])
                a = 1/ difs[d]
                old_value = difs[d]
                propper_value = all_data[variable_to_calculate][d]
                dif = old_value - propper_value;
                sum_error += dif
                working_dif_count += 1
            except:
                pass
        mse = (1/working_dif_count) * (sum_error ** 2)
        return mse

    def compare_against_true_value(self):
        if self.output == (all_data[variable_to_calculate][self.neurons_index]):
     #       print("bugger me first match ")
            print(9/0)
        else:
            if type(self.output) != str:
                A = self.output - all_data[variable_to_calculate][self.neurons_index]
     #           print(A)
                return A
            else:
                return 99999999999999999999999999999999999999999999

    def print_this_neurons_stuff(self):
        pass
       # print(self.this_neurons_operation_despription)


       # for bracket in self.equation_chunks:
        #    print("          bracket          ")
         #   print("     weight      ,       bias        ,     variable    ,    indices    ,     function      ")
          #  for index in range(len(bracket["weights"])):
           #     print(str(bracket["weights"][index]) + "      ,      " + str(bracket["biases"][index])+ "      ,        " + str(bracket["variables"][index])+ "        ,           " + str(bracket["indices"][index]) + "     ,    "+ str(bracket['function'][index])+ "     ,    "+ str(bracket['variable_names'][index]) )


class Layer:
    def __init__(self , layer_num , layer_population , first = False , previous_best_neuron = 0):
       # print("meking new layer 777777777777777777777777777777777777777777777777777777777777777777")
        
        if first:
            self.this_layer = []
            for new_neuron in range(layer_population):
                self.this_layer.append(neuron(first))
        else:
            hard_copy_of_good_neuron = copy.deepcopy(previous_best_neuron)
            self.this_layer = []
            for new_neuron in range(layer_population):
                hard_copy_of_good_neuron = copy.deepcopy(previous_best_neuron)
                self.this_layer.append(neuron(False , hard_copy_of_good_neuron))


    def forward(self):
        for n in self.this_layer:
            n.forward()

    def find_best_neuron(self):
        best_mse = 99999999999999999999999999999999
        best_neuron = ""
     #   print("lmf")
        for n in self.this_layer:
    #        print("checking best for this " + str(n.this_neurons_operation_despription))
            if (not  isinstance(n.output, complex)):
                mse = n.mean_squared_error()
        #        print(str(n.output)+ "    =     n.output")
                if mse < best_mse:
                    best_neuron = n
                    best_mse = mse
                else:
                    pass
        #            print(str(mse) + "    mse too big")
            else:
                pass
   #             print(str(n.output) + "        n.output is complex ")

  #      print("lmf atl")

 #       print(str(best_mse)+ "      best mse ")
        if (type(best_neuron) == str):
        #    print("literally no good neuron start ")
         #   for n in self.this_layer:
          #      print("checking best for this " + str(n.this_neurons_operation_despription))
  #              mse = n.mean_squared_error()
 #               print(mse)
       #     print("literally no good neuron end ")
            return "literally no good neuron end ";
        return best_neuron


    def describe_layer(self):
        for n in self.this_layer:
     #       print("new neuron ###############")
            n.print_this_neurons_stuff();



#describe_layer(

#while 1 == 1:

 #   print("AAAA----------1")
#
 #   uno = Layer(1, 2 , True)
  #  print("AAAA----------2")
#
 #   uno.describe_layer()
  #  print("AAAA----------3")
#
 #   uno.forward()
  #  best_neuron = uno.find_best_neuron()
#
 #   print(best_neuron.bracket_operations)
  #  print("best = "+ str(best_neuron.this_neurons_operation_despription))
   # best_mse = best_neuron.mean_squared_error();
#
 #   print("BBBB----------4")
  #  new_layer = Layer(2 , 2 , False , best_neuron)
   # print("BBBB----------5")
    #new_layer.describe_layer()
   # print("BBBB----------6")


 #   best_neuron = new_layer.find_best_neuron()
#    best_mse = best_neuron.mean_squared_error();

#print(1/0)
#  .output


max_counter = 0
best_ever_mse = 9999999999999
fail_counter = 0

while 1==1:
#    try:
    reset = False
    best_layer = Layer(1, base_layer_pop , True)
 #   print(" 999999999999999 step 1")
    best_layer.forward()

  #  print(" 999999999999999  step 2 ")
    best_neuron = best_layer.find_best_neuron()
   # print(" 999999999999999  step 2.5 ")

    try:
        best_neuron.print_this_neurons_stuff()
    except:
        print(str(best_neuron)+ "      fail        ")
        print(9/0)


    best_mse = best_neuron.mean_squared_error();
    #print(str(best_mse)+ " =   freshly set best_mse")
    all_mses = [best_mse]

    finaldf = pd.DataFrame({'counter':[],'mse':[],'full operation':[], 'full operation values':[],  })
    newrow = pd.DataFrame({'counter':[str(0)],'mse':[str(best_mse)],'full operation':[best_neuron.this_neurons_operation_despription], 'full operation values':[best_neuron.bracket_values()]  })
    finaldf.append(newrow)

    counter = 0
    while best_mse != 0 and reset == False:
        print(str(counter) + "                   = counter ")
        counter += 1
        max_counter += 1
 #       print(" 999999999999999 ")
        new_layer = Layer(2 , subsequent_layer_pop , False , best_neuron)
        new_layer.forward()
        new_best_neuron = new_layer.find_best_neuron()
        if type(new_best_neuron) == str:
            if new_best_neuron == "literally no good neuron end ":
                print(1/0)
                reset = True

        print("--------------------------- 0909090909090909909 ----------------------------------")
        print(new_best_neuron.this_neurons_operation_despription)
        print("--------------------------- 22222222222444444422222222222 ----------------------------------")

        if not reset:
            new_mse = new_best_neuron.mean_squared_error();

            if new_mse < best_mse:
                best_mse = new_mse
                best_neuron = new_best_neuron
   #             for i in range(5):
  #                  print(str(new_mse)+ "             new best_mse")
            else:
    #            for i in range(5):
     #               print(str(new_mse)+ " = bad new mse   ,   which aint as good as = "+ str(best_mse))
                reset = True

            if new_mse < best_ever_mse:
      #          print(" ")
                best_ever_mse = new_mse
                special_row = pd.DataFrame({'counter':[str(counter)],'mse':[str(new_mse)],'full operation':[new_best_neuron.this_neurons_operation_despription],  'full operation values':[best_neuron.bracket_values()] })
                finaldf = finaldf.append(special_row)
                finaldf.to_csv(str(new_mse)+"_best_ever_mse.csv")

            if not reset:
                
                all_mses.append(new_mse)

                newrow = pd.DataFrame({'counter':[str(counter)],'mse':[str(new_mse)],'full operation':[new_best_neuron.this_neurons_operation_despription] , 'full operation values':[best_neuron.bracket_values()]  })
                finaldf = finaldf.append(newrow)
                if counter > 150:
                    finaldf.to_csv("good sequential attempts ="+str(counter)+"     total rounds = "+str(max_counter)+".csv")
                fail_counter = 0
                
#         print("waaaaaay")
#           time.sleep(3)
##########################################################################
#    except:
      #  fail_counter+=1
 #       for k in range(4):
  #          print("bugaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa ")
    #    if (fail_counter > 30):
     #       print(9/0)
