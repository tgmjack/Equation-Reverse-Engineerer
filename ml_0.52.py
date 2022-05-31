import copy
import random
import numpy
import pandas as pd
import time
import sys

#### have optional constants (it looks like its just optimizing the constants)
####  change last_100 measurer to last_x iterations

################ add controlable error where all zero div errors mean its impossible
################ chance_to_remove_inner_term = 1;      doesnt seem to work   (double check )

######################################## managing math sysmbols when calcing is problematic
################  None seems to get into maths symvbols (probably just iterating too far )
sys.setrecursionlimit(10000)

max_inner_bracket_terms = 2
max_mid_bracket_terms = 2
max_outer_bracket_terms = 2

base_layer_pop = 10000
subsequent_layer_pop = 200

chances_to_add_term = 1
probability_to_add_term = 0.05

chance_to_remove_inner_term = 0.05;
chance_to_remove_mid_term = 0.05
chance_to_remove_outer_term = 0.05

chance_to_change_inner_polynomial = 0.05;
chance_to_change_inner_variable = 0.05;
chance_to_change_inner_indices = 0.05;
chance_to_change_inner_constant = 0.05;
chance_to_change_inner_mathematical_function = 0.05;


chance_to_change_mid_polynomial = 0.05;
chance_to_change_mid_indices = 0.05;
chance_to_change_mid_constant = 0.05;
chance_to_change_mid_mathematical_function = 0.05;

chance_to_change_outer_polynomial = 0.05;
chance_to_change_outer_indices = 0.05;
chance_to_change_outer_constant = 0.05;
chance_to_change_outer_mathematical_function = 0.05;



variable_to_calculate = "v"

variables = ["s","u","v" , "a" , "t" ]

ss = [10, 3 , 2.4 , 19.03842 ,0.5 , 1 , 3 , 9 , 15 , 10027.500182281841, 1100.899946]
us = [1 , 9 , -3 , 1 , 90 , 2 , 2 , 8 , 60 , -82499.333 , 1100899.94]
vs = [0 , 3 , 9 , 0.1 , 1 , 3 , 1 , 7 , 80 , 82500.67 , 1100899.952]
a_s = [-0.05 , -12 , 15 , -0.026 , -8099 , 2.5 , -0.5 , -0.833 , 93.33 , 11 , 12]
ts = [20 , 0.5 , 0.8 , 34.61538461538462, 0.01098901098901099 , 0.4 , 2 , 1.2004801920768309 , 0.21429336762027215, 15000.000272727273 , 0.001000000008692344]

all_data = [ss , us , vs , a_s , ts]
all_data = {'s':ss, 'u':us, 'v':vs, 'a':a_s, 't':ts}


def test_equation():
    # v=u+at     =       t = (v-u)/A
    error = 0
    for d in range(len(ss)):
        t = (vs[d] - us[d]) / a_s[d]
        print(" diff  =  "+str(t - ts[d]))
        error += (t - ts[d])**2
    e = error
    print(e)
   # print(10/0)
def test_equation2():
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

#test_equation()
#print(9/0)

class inner_bracket_chunks:
    def __init__(self , polynomials , variables , indices , constants , mathematical_functions):
        self.polynomials = polynomials
        self.variables = variables
        self.indices = indices
        self.constants = constants
        self.mathematical_functions = mathematical_functions

class outer_bracket_chunks:
    def __init__(self , polynomials , mid_brackets , indices , constants , mathematical_functions):
        self.polynomials = polynomials
        self.mid_brackets = mid_brackets
        self.indices = indices
        self.constants = constants
        self.mathematical_functions = mathematical_functions

# mid_bracket_chunks(mid_polynomials , mid_inner_brackets, mid_indices , mid_constants , mid_mathematical_function)
class mid_bracket_chunks:
    def __init__(self , polynomials , inner_brackets , indices , constants , mathematical_functions):
        self.polynomials = polynomials
        self.inner_brackets = inner_brackets
        self.indices = indices
        self.constants = constants
        self.mathematical_functions = mathematical_functions



class neuron:
    def get_random_stuff(poynomial_bool = True , variable_bool = True, indices_bool = True, constant_bool = True , mathematical_function_bool = True):
        #### this function is used to choose random terms, this function is usually used to start off our equation
        cleaned_variables = copy.deepcopy(variables)
        cleaned_variables.remove(variable_to_calculate)
        var = "not set"; polynomial = "not set"; indices = "not set"; constant = "not set"; math_func = "not set";
        if variable_bool:
            var_ind = random.randint(0, len(cleaned_variables)-1)
            var = cleaned_variables[var_ind]
        if poynomial_bool:
            polynomial = random.randint(0,3)
        if indices_bool:
            indices = random.randint(0,3)
        if constant_bool:
            constant = random.randint(0,3)
        if mathematical_function_bool:
            math_func_chooser = random.randint(0,3)
            if math_func_chooser == 0:
                math_func = "-"
            elif math_func_chooser == 1:
                math_func = "+"
            elif math_func_chooser == 2:
                math_func = "*"
            elif math_func_chooser == 3:
                math_func = "/"
            else:
                print("this should never happen   66666 ")
        return var , polynomial , indices , constant , math_func;

    def update_this_variable(self , og_var):
        cleaned_variables = copy.deepcopy(variables)
   #     print(variable_to_calculate)
    #    print(og_var)
        cleaned_variables.remove(variable_to_calculate)
        cleaned_variables.remove(og_var)
        var_ind = random.randint(0, len(cleaned_variables)-1)
        var = cleaned_variables[var_ind]
        return var;

    def update_this_term(self , og_term):
        term_update_chooser = random.random()
        if term_update_chooser<0.1:
            term = 0
        elif term_update_chooser<0.2:
            term = 1
        elif term_update_chooser<0.3:
            term = 2
        elif term_update_chooser<0.6:
            term = og_term+random.random()
        elif term_update_chooser<0.9:
            term = og_term-random.random()
        else:
            try:
                term = 1/og_term
            except:
#                print("tried inverting term but faled ")
                term = og_term
#                handle_div_zero_error()
        return term;

    def update_this_mathematical_function(self , og_func):
        pass

    def evolve_parent(self , parent_neuron):
        new_neuron = copy.deepcopy(parent_neuron)
############################################################# choose what to remove
        outer_index_to_remove = []
        mid_index_to_remove = []
        inner_index_to_remove = []
        for mi, outer_index in zip(new_neuron.outer_bracket_chunks.mid_brackets , range(len(new_neuron.outer_bracket_chunks.polynomials))):
            for (inner , mid_index) in zip(mi.inner_brackets , range(len(mi.inner_brackets))):
                for inner_index in range(len(inner.polynomials)):
                    this_chance_to_remove_inner_term = random.random()
                    if this_chance_to_remove_inner_term < chance_to_remove_inner_term:
                        inner_index_to_remove.append([outer_index, mid_index, inner_index])
                this_chance_to_remove_mid_term = random.random()
                if this_chance_to_remove_mid_term < chance_to_remove_mid_term:
                    mid_index_to_remove.append([outer_index, mid_index])
            this_chance_to_remove_outer_term = random.random()
            if this_chance_to_remove_outer_term < chance_to_remove_outer_term:
                outer_index_to_remove.append([outer_index])

###################### remove inner components below
        for inner_to_remove in reversed(inner_index_to_remove):   # removing by index is impossible forwards
            #### if not last element remove a math func (cos there is no math func at end )
      #      print("removing inner ")
            if inner_to_remove[2] < len(new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].mathematical_functions):
    #            print(" booooooooo ")
#                print(inner_to_remove[2])
                new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].mathematical_functions.pop(inner_to_remove[2])
            #### remove rest of stuff stuff
#            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials.remove(new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials[inner_to_remove[2]])
  #          print("booooooo ")
 #           print(inner_to_remove[1])

#            print(inner_to_remove[2])
#
#            for a in new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials:
#                print("before a = "+str(a))
#                print("to remove   "+str(inner_to_remove[2]))
            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials.pop(inner_to_remove[2])

#            for a in new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials:
#                print("after a = "+str(a))

#            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].variables.remove(new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].variables[inner_to_remove[2]])
            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].variables.pop(inner_to_remove[2])
#            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].indices.remove(new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].indices[inner_to_remove[2]])

       #     for a in new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].indices:
        #        print("before b = "+str(a))
            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].indices.pop(inner_to_remove[2])
         #   for a in new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].indices:
          #      print("after b = "+str(a))
#            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].constants.remove(new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].constants[inner_to_remove[2]])
            new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].constants.pop(inner_to_remove[2])


########### check if any of mids inners are empty below, if they are the mids have to be removed too


        mid_index_to_remove = []
        for mi, outer_index in zip(new_neuron.outer_bracket_chunks.mid_brackets , range(len(new_neuron.outer_bracket_chunks.polynomials))):
            for (inner , mid_index) in zip(mi.inner_brackets , range(len(mi.inner_brackets))):
                if len(inner.polynomials) == 0:
                    mid_index_to_remove.append([outer_index, mid_index])
#        for mi, outer_index in zip(new_neuron.outer_bracket_chunks.mid_brackets , range(len(new_neuron.outer_bracket_chunks.polynomials))):
#            for (inner , mid_index) in zip(mi.inner_brackets , range(len(mi.inner_brackets))):
#                print(str(outer_index)+ "     "+str(mid_index)+ "      =       what exists ")
#        for mid_to_remove in mid_index_to_remove:
#            print(str(mid_to_remove[0])+"     ,     "+str(mid_to_remove[1])+"   what were gunna try to remove")
        for mid_to_remove in reversed(mid_index_to_remove):
            #### if not last element remove a math func (cos there is no math func at end )
#            for mf in new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].inner_brackets[mid_to_remove[1]].mathematical_functions:
#                print(mf)
            if mid_to_remove[1] < len(new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].inner_brackets[mid_to_remove[1]].mathematical_functions):
                new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].mathematical_functions.pop(mid_to_remove[1])

            new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].polynomials.pop(mid_to_remove[1])
            new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].inner_brackets.pop(mid_to_remove[1])
            new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].indices.pop(mid_to_remove[1])
            new_neuron.outer_bracket_chunks.mid_brackets[mid_to_remove[0]].constants.pop(mid_to_remove[1])



########### if middles are empty then outers has to be removed

        outer_index_to_remove = []
        for mi, outer_index in zip(new_neuron.outer_bracket_chunks.mid_brackets , range(len(new_neuron.outer_bracket_chunks.polynomials))):
            if len(mi.polynomials) == 0:
                outer_index_to_remove.append([outer_index])

        for outer_to_remove in reversed(outer_index_to_remove):
            #### if not last element remove a math func (cos there is no math func at end )
            if outer_to_remove[0] < len(new_neuron.outer_bracket_chunks.mathematical_functions):
                new_neuron.outer_bracket_chunks.mathematical_functions.pop(outer_to_remove[0])
            new_neuron.outer_bracket_chunks.polynomials.pop(outer_to_remove[0])
            new_neuron.outer_bracket_chunks.mid_brackets.pop(outer_to_remove[0])
            new_neuron.outer_bracket_chunks.indices.pop(outer_to_remove[0])
            new_neuron.outer_bracket_chunks.constants.pop(outer_to_remove[0])


##########    add new inner terms below
# new_neuron.outer_bracket_chunks.mid_brackets[inner_to_remove[0]].inner_brackets[inner_to_remove[1]].polynomials

        for chance_to_add_term in range(chances_to_add_term):
            this_probability_to_add_term = random.random()
            if this_probability_to_add_term < probability_to_add_term:
                if len(new_neuron.outer_bracket_chunks.mid_brackets) > 0:
            #        print(new_neuron.outer_bracket_chunks.mid_brackets)
                    outer_ind = random.randint(0, len(new_neuron.outer_bracket_chunks.mid_brackets)-1)
                    mid_ind = random.randint(0, len(new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets)-1)
                    inner_ind = random.randint(0, len(new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].polynomials)-1)
                    var , polynomial , indices , constant , math_func = self.get_random_stuff()
           #         print(" were adding a thing ")
                    new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].mathematical_functions.insert(inner_ind-1 , math_func)
                    new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].polynomials.insert(inner_ind , polynomial)
                    new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].variables.insert(inner_ind , var)
                    new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].indices.insert(inner_ind , indices )
                    new_neuron.outer_bracket_chunks.mid_brackets[outer_ind].inner_brackets[mid_ind].constants.insert(inner_ind , constant )
                elif len(new_neuron.outer_bracket_chunks.mid_brackets) == 0:
                    var , polynomial , indices , constant , math_func = self.get_random_stuff()
                    these_inner_bracket_chunks = inner_bracket_chunks([polynomial] , [var], [indices] , [constant] , [math_func])
                    var , mid_polynomial , mid_indices , mid_constant , mid_math_func = self.get_random_stuff()
                    these_mid_bracket_chunks = mid_bracket_chunks([mid_polynomial] , [these_inner_bracket_chunks], [mid_indices] , [mid_constant] , [mid_math_func])
                    var , out_polynomial , out_indices , out_constant , out_math_func = self.get_random_stuff()
                    these_out_bracket_chunks = outer_bracket_chunks([out_polynomial] , [these_mid_bracket_chunks], [out_indices] , [out_constant] , [out_math_func])
                    new_neuron.outer_bracket_chunks= these_out_bracket_chunks


# var , polynomial , indices , constant , math_func;
#var = cleaned_variables[var_ind]

            # random mid_bracket
            # random inner bracket
            # random position in here for before first to after last
            # add random term in that position

###########     slight updates on existing equation terms below
###########     ffffffffffffff

        for mi, outer_index in zip(new_neuron.outer_bracket_chunks.mid_brackets , range(len(new_neuron.outer_bracket_chunks.polynomials))):
            for (inner , mid_index) in zip(mi.inner_brackets , range(len(mi.inner_brackets))):
                for inner_index in range(len(inner.polynomials)):
                    inner_polynomial_update_chooser = random.random()
                    if inner_polynomial_update_chooser < chance_to_change_inner_polynomial:
                        inner.polynomials[inner_index]= self.update_this_term(inner.polynomials[inner_index])
                    inner_variables_update_chooser = random.random()
                    if inner_variables_update_chooser < chance_to_change_inner_variable:
                        inner.variables[inner_index]= self.update_this_variable(inner.variables[inner_index])
                    inner_indices_update_chooser = random.random()
                    if inner_indices_update_chooser < chance_to_change_inner_indices:
             #           print("update indices")
                        inner.indices[inner_index]= self.update_this_term(inner.indices[inner_index])
                    inner_constants_update_chooser = random.random()
                    if inner_constants_update_chooser < chance_to_change_inner_constant:
                        inner.constants[inner_index]= self.update_this_term(inner.constants[inner_index])
                    inner_math_func_update_chooser = random.random()
                    if inner_math_func_update_chooser < chance_to_change_inner_mathematical_function:
                        if inner_index < len(inner.mathematical_functions):
                            inner.mathematical_functions[inner_index]= self.update_this_mathematical_function(inner.mathematical_functions[inner_index])    ####

#########

                mid_polynomial_update_chooser = random.random()
                if mid_polynomial_update_chooser < chance_to_change_mid_polynomial:
                    mi.polynomials[mid_index]= self.update_this_term(mi.polynomials[mid_index])
                mid_indices_update_chooser = random.random()
                if mid_indices_update_chooser < chance_to_change_mid_indices:
                    mi.indices[mid_index]= self.update_this_term(mi.indices[mid_index])
                mid_constants_update_chooser = random.random()
                if mid_constants_update_chooser < chance_to_change_mid_constant:
                    mi.constants[mid_index]= self.update_this_term(mi.constants[mid_index])
                mid_math_func_update_chooser = random.random()
                if mid_math_func_update_chooser < chance_to_change_mid_mathematical_function:
                    if mid_index < len(mi.mathematical_functions):
                        mi.mathematical_functions[mid_index]= self.update_this_mathematical_function(mi.mathematical_functions[mid_index])

######################################################################################   update outer chunks below
        for out_p, out_i, out_c in zip(new_neuron.outer_bracket_chunks.polynomials,new_neuron.outer_bracket_chunks.indices,new_neuron.outer_bracket_chunks.constants):
            outer_polynomial_update_chooser = random.random()
            if outer_polynomial_update_chooser < chance_to_change_outer_polynomial:
                out_p= self.update_this_term(out_p)
            outer_indices_update_chooser = random.random()
            if outer_indices_update_chooser < chance_to_change_outer_indices:
                out_i= self.update_this_term(out_i)
            outer_constants_update_chooser = random.random()
            if outer_constants_update_chooser < chance_to_change_outer_constant:
                out_c= self.update_this_term(out_c)
        for math_func in new_neuron.outer_bracket_chunks.mathematical_functions:
            outer_math_func_update_chooser = random.random()
            if outer_math_func_update_chooser < chance_to_change_outer_mathematical_function:
                if outer_index < len(new_neuron.outer_bracket_chunks.mathematical_functions):
                    math_func= self.update_this_mathematical_function(math_func)
#####################################

        return new_neuron.outer_bracket_chunks;

    def __init__(self , parent_neuron = 0   ,neuron_num =0 , layer_num = 0  ):

        if parent_neuron == 0:  #### if there is no parent, we have to create this neuron from scratch
            outer_mid_brackets, outer_polynomials, outer_indices , outer_constants , outer_mathematical_functions = [],[],[],[],[]
            for o in range(max_outer_bracket_terms):
       #         print(str(o)+ "   o  ")
                mid_inner_brackets, mid_polynomials, mid_indices , mid_constants , mid_mathematical_functions = [],[],[],[],[]
                for m in range(max_mid_bracket_terms):
                    variables, polynomials, indices , constants , mathematical_functions = [],[],[],[],[]
        #            print(str(m)+ "   m  ")
                    for i in range(max_inner_bracket_terms):
                        inner_var , inner_polynomial , inner_power , inner_constant , inner_mathematical_function = self.get_random_stuff();
                        polynomials.append(inner_polynomial)
        #                print(str(i) + "   i   ")
                        variables.append(inner_var)
                        indices.append(inner_power)
                        constants.append(inner_constant)
                        if len(variables) - len(mathematical_functions) == 2:
                            mathematical_functions.append(inner_mathematical_function)
        #                    print(" goooooo dddddddd    "+str(inner_mathematical_function))
                    these_inner_bracket_chunks = inner_bracket_chunks(polynomials , variables, indices , constants , mathematical_functions)
                    mvar , mpolynomial , mpower , mconstant , mmathematical_function = self.get_random_stuff(variable_bool = False)
                    mid_polynomials.append(mpolynomial)
                    mid_indices.append(mpower)
                    mid_constants.append(mconstant)
                    if len(mid_indices) - len(mid_mathematical_functions) == 2:
                        mid_mathematical_functions.append(mmathematical_function)
           #             print(" goooooo dddddddd 2 ")
                    mid_inner_brackets.append(these_inner_bracket_chunks)
                these_mid_bracket_chunks = mid_bracket_chunks(mid_polynomials , mid_inner_brackets, mid_indices , mid_constants , mid_mathematical_functions)
                var , polynomial , power , constant , mathematical_function = self.get_random_stuff(variable_bool = False)
                outer_polynomials.append(polynomial)
                outer_indices.append(power)
                outer_constants.append(constant)
                if len(outer_indices) - len(outer_mathematical_functions) == 2:
                    outer_mathematical_functions.append(mathematical_function)
            #        print(" goooooo dddddddd 3 ")
                outer_mid_brackets.append(these_mid_bracket_chunks)

            self.outer_bracket_chunks = outer_bracket_chunks(outer_polynomials , outer_mid_brackets, outer_indices , outer_constants , outer_mathematical_functions)
            self.neuron_num = neuron_num
            self.layer_num = layer_num
            self.parent_neuron = parent_neuron
     #       print("after creation check ")
            #for m in range(len(self.outer_bracket_chunks.mid_brackets)):
            #    print("    m start   "+str(m))
           #     for i in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets)):
          #          print("   m = "+str(m) + "   i = "+str(i) )
         #           for maths_sym , math_sym_counter in zip(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions , range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions))):
        #                print(str(maths_sym)+ "        math_sym_counter " +str( math_sym_counter))
       #             for poly , poly_counter in zip(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials , range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials))):
      #                  print(str(poly)+ "        poly_counter " +str(poly_counter))

        elif parent_neuron != 0:
            self.outer_bracket_chunks = self.evolve_parent(parent_neuron = parent_neuron)
            self.neuron_num = neuron_num
            self.layer_num = layer_num
            self.parent_neuron = parent_neuron


    def describe_neurons_evolution(self):
        the_neuron_were_currently_using = self
        print("start describing history")
        whole_history = " @@@@@@@@@@@@@@@@@@ "
        while the_neuron_were_currently_using.parent_neuron != 0:
            print(" ")
            whole_history += the_neuron_were_currently_using.describe_neuron()
            whole_history += " @@@@@@@@@@@@@@@@@@ "
            the_neuron_were_currently_using = the_neuron_were_currently_using.parent_neuron
        print("finished describing history")
        return whole_history

    def describe_neuron(self , deep_describe = False):
        txt = ""
        txt += " ( "


        if deep_describe:
            deep_describe_txt_inner = " [ "
            deep_describe_txt_mid = " [ "
            deep_describe_txt_header = "  poly     ,    power     , constant "
            deep_describe_txt_outer = " [ "
            for outer_p, outer_I , outer_c , m in zip(self.outer_bracket_chunks.polynomials, self.outer_bracket_chunks.indices , self.outer_bracket_chunks.constants  , self.outer_bracket_chunks.mid_brackets):
                deep_describe_txt_outer += str(outer_p) + " , " +str(outer_I) + " , " + str(outer_c)+ "    ----------------   "
                for mid_p, mid_I , mid_c , I in zip(m.polynomials, m.indices , m.constants  , m.inner_brackets):
                    deep_describe_txt_mid += str(mid_p) + " , "+ str(mid_I) + " , " + str(mid_c)+ "    ----------------   "
                    for  in_p, in_I , in_c , in_v in zip(I.polynomials, I.indices , I.constants  , I.variables):
                        deep_describe_txt_inner += str(in_p) + " , "+ str(in_I) + " , " + str(in_c) + " , " + str(in_v)+ "    ----------------   "

            print(deep_describe_txt_header)
            print(deep_describe_txt_outer)
            print(deep_describe_txt_mid)
            print(deep_describe_txt_inner)

        for m in range(len(self.outer_bracket_chunks.mid_brackets)):
            txt += " (  _"+str(self.outer_bracket_chunks.polynomials[m])
            txt += "  (  "
            for i in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets)):
                txt += " ( "+str(self.outer_bracket_chunks.mid_brackets[m].polynomials[i])
                txt += "  (  "

                for inner_index in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials)):

                    if inner_index < len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions):
                        print(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                for inner_index in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials)):
                    txt += " ( " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index])
                    txt += "  (  " + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]
                    txt += "  **  " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + " ) "
                    txt += "  +  " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index])
                    txt += " ) "
                    if inner_index < len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions):

                        if type(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]) != type(None):
                            txt += "  "+self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]
            #            print(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index] + " wtf m = "+str(m)+ "   i = "+str(i)+ "   inner index = "+str(inner_index))
            #            print("   aaaaaaa    ")
            #    txt+= "wtf"
##################################################################
                txt += "  **  "+str(self.outer_bracket_chunks.mid_brackets[m].indices[i]) + " ) "
                txt += "  +  "+str(self.outer_bracket_chunks.mid_brackets[m].constants[i])
                txt += " )  "
                if i < len(self.outer_bracket_chunks.mid_brackets[m].mathematical_functions):
                    if type(self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i])  != type(None):
                        txt += "  "+self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]
            txt += "  **  "+str(self.outer_bracket_chunks.indices[m]) + " ) "
            txt += "  +  "+str(self.outer_bracket_chunks.constants[m])
            txt += " ) "
            if m < len(self.outer_bracket_chunks.mathematical_functions):
                if type(self.outer_bracket_chunks.mathematical_functions[m])  != type(None):
                    txt += "  "+self.outer_bracket_chunks.mathematical_functions[m]
    #    print("jhkl,hg")
        print(txt)
        return txt

    def perform_calculation_at_data_index(self , index , return_bits = False):

        all_individual_bits ="( "
        try:
            complete_total = 0
            for m in range(len(self.outer_bracket_chunks.mid_brackets)):
                this_mid_total = 0
                for i in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets)):
                    this_inner_total = 0
                    for inner_index in range(len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials)):
                        if this_inner_total == 0:
                            this_inner_total = self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]
                            if return_bits:
                                all_individual_bits +="     ===== " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) + " ======  because    p = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]) + "   v =  "+ str(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index]) + "       power = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index])+ "       constant = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index])

                #            print(str(this_inner_total)+ "          this_inner_total 1 ")
                        else:
                            if inner_index < len(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions):
                                if "+" == self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]:
                                    this_inner_total += self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]
                                    if return_bits:
                                        all_individual_bits +="   =====  " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) + " ======  because    p = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]) + "   v =  "+ str(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index]) + "       power = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index])+ "       constant = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) +str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                                elif "-" == self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]:
                                    this_inner_total += -(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index])
                                    if return_bits:
                                        all_individual_bits +="   =====  " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) + " ======  because    p = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]) + "   v =  "+ str(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index]) + "       power = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index])+ "       constant = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) +str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                                elif "*" == self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]:
                                    this_inner_total = this_inner_total * (self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index])
                                    if return_bits:
                                        all_individual_bits +="    ===== " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) + " ====== because    p = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]) + "   v =  "+ str(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index]) + "       power = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index])+ "       constant = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) +str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                                elif "/" == self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index]:
                                    this_inner_total = this_inner_total / (self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index])
                                    if return_bits:
                                        all_individual_bits +="   =====  " + str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]*(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index] ** self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index]) + self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) + " ======  because    p = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].polynomials[inner_index]) + "   v =  "+ str(all_data[self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].variables[inner_index]][index]) + "       power = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].indices[inner_index])+ "       constant = "+str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].constants[inner_index]) +str(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                                else:
                                #    print(self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions[inner_index])
                               #     print([inner_index])
                              #      for mf in self.outer_bracket_chunks.mid_brackets[m].inner_brackets[i].mathematical_functions:
                             #           print(mf)
                                    print("this just shouldnt happen ")
                                    print(5/0)
                 #       print(str(this_inner_total)+ "     this_inner_total 2")

                    if this_mid_total == 0:
                        this_mid_total = self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i]
                    else:
                        if i < len(self.outer_bracket_chunks.mid_brackets[m].mathematical_functions):
                            if "+" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                                this_mid_total += self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i]
                            elif "-" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                                this_mid_total += -(self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
                            elif "/" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                                this_mid_total = this_mid_total / (self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
                            elif "*" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                                this_mid_total = this_mid_total * (self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
           #         print(str(this_mid_total)+ "     this_mid_total")

                ######
                if complete_total == 0:
                    complete_total = self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_mid_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i]
                else:
                    if m < len(self.outer_bracket_chunks.mid_brackets[m].mathematical_functions):
                        if "+" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                            complete_total += self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i]
                        elif "-" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                            complete_total += -(self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
                        elif "/" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                            complete_total = complete_total / (self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
                        elif "*" == self.outer_bracket_chunks.mid_brackets[m].mathematical_functions[i]:
                            complete_total = complete_total * (self.outer_bracket_chunks.mid_brackets[m].polynomials[i]*(this_inner_total ** self.outer_bracket_chunks.mid_brackets[m].indices[i]) + self.outer_bracket_chunks.mid_brackets[m].constants[i])
            #    print(str(complete_total)+ "     complete_total")
            if return_bits:
                return complete_total, all_individual_bits

            return complete_total;
        except ZeroDivisionError as error:
            for ting in range(1):
                print("  zero div error  ")
            return " zero div error ";

    def get_error_at_this_index(self, index):

        current_answer = self.perform_calculation_at_data_index(index)
  #      print("actual calculation for = "+str(variable_to_calculate)+ "         =   "+str(current_answer)+ "       at index = "+str(index))
        if type(current_answer) == type("lol"):
            return "erorr finding error"

        error = abs(all_data[variable_to_calculate][index]-current_answer)
   #     print(str(error)+" =   error      cos  "+str(all_data[variable_to_calculate][index]) + " - " + str(current_answer))
        return error;
    def get_rmse(self):
        total_square_error = 0
        error = "not set"
        for data_index in range(len(all_data[variable_to_calculate])):
            try:
                error = self.get_error_at_this_index(data_index)
    #            print(str(error) + " error          at          index  "+str(data_index))
            except OverflowError as theerror:
         #       print("if the error is too big to calculate then screw it")
                rmse = 999999999999999999999999999999999999999

            if type(error) == type("lol"):
                return "error finding error"
            try:
                error_squared = error ** 2
                if error_squared < 0:
                    print(8/0)
                total_square_error+= error_squared

            except OverflowError as theerror:
   #             print("if the error is too big to calculate then screw it")
                rmse = 999999999999999999999999999999999999999
        try:
       #     print(str(total_square_error)+ "    total_square_error")
            total_square_error_over_num_of_elems = total_square_error / len(all_data[variable_to_calculate])
            rmse = total_square_error_over_num_of_elems ** 0.5
        except OverflowError as theerror:
    #        print("if the error is too big to calculate then screw it")
            rmse = 99999999999999999999999999999999999999999
        return rmse

class Layer:
    def __init__(self , population, layer_num, parent_neuron = 0):
        self.neurons = []
        self.layer_num = layer_num;
        neuron_num_counter = 0
        if parent_neuron == 0:
            ### (self , parent_neuron = 0   ,neuron_num =0 , layer_num = 0  )
            for pop in range(population):
                neuron_num_counter+= 1
                self.neurons.append(neuron(parent_neuron = parent_neuron ,neuron_num = neuron_num_counter ,  layer_num = layer_num))
        else:
            for pop in range(population):
                neuron_num_counter+= 1
                self.neurons.append(neuron(parent_neuron = parent_neuron ,neuron_num = neuron_num_counter  ,  layer_num = layer_num))

    def find_best_rmse_in_layer(self):
        best_rmse = 9999999999999999999999999999999999999999999999
        best_neuron = "none worked"
        for neuron in self.neurons:
            this_rmse = neuron.get_rmse()
            if type(this_rmse) == type("lol"):
                this_rmse = 99999999999999999999999999999999999999999999999999
            if this_rmse < best_rmse:
                best_rmse = this_rmse
                best_neuron = neuron
        return best_neuron



comment_out = '''
#uno = neuron(parent_neuron = 0 ,neuron_num = 0 ,  layer_num = 0)
#deux = neuron(parent_neuron = uno ,neuron_num = 0 ,  layer_num = 1)
uno = Layer( 2 , layer_num = 0, parent_neuron = 0 )
this_best_neuron = uno.find_best_rmse_in_layer()
deux = neuron(parent_neuron = this_best_neuron ,neuron_num = 0 ,  layer_num = 1)
this_neuron = deux
while this_neuron != 0:
    print(str(this_neuron.neuron_num)+" mneuron num                     layer num "+str(this_neuron.layer_num))
    this_neuron = this_neuron.parent_neuron
    print("yo")
print(9/0) '''


def make_specific_neuron():


##### somehow v = u+at = just a


    mi_neuron = neuron(parent_neuron = 0 ,neuron_num = 0 ,  layer_num = 0)
    inner_u = inner_bracket_chunks([1],['u'],[1],[0],[])
    inner_a_t = inner_bracket_chunks([1,1],['a','t'],[1,1],[0,0],['*'])
    mid_chunk = mid_bracket_chunks([1,1], [inner_u, inner_a_t], [1,1] , [0,0] , ['+'])
    mi_neuron.outer_bracket_chunks = outer_bracket_chunks([1],[mid_chunk],[1],[0],[])   #   = this now has v = u + at
    print(mi_neuron.get_rmse())
    mi_neuron.describe_neuron(True)
    print(9/0)

# make_specific_neuron()

def reset():
    layer_num_counter = 0
    layer1 = Layer(base_layer_pop , layer_num_counter)
    this_best_neuron = layer1.find_best_rmse_in_layer()
    last_rmse = this_best_neuron.get_rmse();
    print("now reset")
    return layer_num_counter, this_best_neuron , last_rmse

import time
import multiprocessing
from multiprocessing import Process, Manager , freeze_support
from datetime import datetime

# Getting the current date and time


def run_function():
    this_rmse = 9999999999;
    big_counter = 0
    while this_rmse != 0:
    #    try:
        last_100_rmse = 999999999
        big_counter+= 1
        print(" big counter   "+str(big_counter))
        layer_num_counter = 0
        ###     , population, layer_num, parent_neuron = 0):
        layer1 = Layer( base_layer_pop , layer_num = layer_num_counter, parent_neuron = 0 )
        this_best_neuron = layer1.find_best_rmse_in_layer()
        this_best_neuron.describe_neuron(True)
        last_rmse = this_best_neuron.get_rmse();
        while 1==1:
            layer_num_counter += 1
            if layer_num_counter%20 == 0:
                if abs(last_100_rmse - this_best_neuron.get_rmse()) < 5: 
                    print("its been 100 iterations and we only changed      "+str(abs(last_100_rmse - this_best_neuron.get_rmse())))
                    print("  not enough rmse change       error resetting     ")
                    layer_num_counter, this_best_neuron , last_rmse = reset()
                else:
                    print("its been 100 iterations and weve changed  " +str(abs(last_100_rmse - this_best_neuron.get_rmse()))+ "    so were good ")
                    last_100_rmse = this_best_neuron.get_rmse()
            print(str(layer_num_counter)+ " ============================================== layer_num_counter   ")
            layer2 = Layer(subsequent_layer_pop , layer_num = layer_num_counter , parent_neuron = this_best_neuron)
       #     for n in layer2.neurons:
        #        print("layer 2  below ")
         #       print(n.describe_neuron(True))
            this_best_neuron = layer2.find_best_rmse_in_layer()


            this_rmse = this_best_neuron.get_rmse();
            #if this_rmse > last_rmse:


        #    this_best_neuron.describe_neurons_evolution();

            if len(this_best_neuron.outer_bracket_chunks.polynomials) == 0:
                print(" empty best neuron ")
                BBB = 0
                this_parent = this_best_neuron
                while this_parent != 0:
                    BBB += 1
                    print("these are the neurons that led to a dead end  "+str(BBB))
                    print(str(this_parent.neuron_num)+" mneuron num                     layer num "+str(this_parent.layer_num))
                    this_parent.describe_neuron(True)
                    this_parent = this_parent.parent_neuron
                print("done showing bad neuron path ")
                layer_num_counter, this_best_neuron , last_rmse = reset()
               # print(9/0)


            if type(this_best_neuron) == type("lol"):
                print("     error resetting     ")
                layer_num_counter, this_best_neuron , last_rmse = reset()
            else:
                this_best_neuron.describe_neuron()
                print(str(this_best_neuron.get_rmse()) + " =   rmse             ,    were good with neuron return  ")

            if this_rmse > last_rmse or this_rmse == last_rmse:
                print("bigger rmse reset ")
                layer_num_counter, this_best_neuron , last_rmse = reset()
            else:
                print("good rmse , improved by = "+str(last_rmse - this_rmse))
                last_rmse = this_rmse

            if this_rmse < 1:
                for i in range(50):
                    print("woah fuck me !!!!!!!!!!!!")
                print("kjhkjh")
                evol = this_best_neuron.describe_neurons_evolution();
                print("kjhkjh    2 ")
                this_best_neuron.describe_neuron(True)
                print("kjhkjh   3")
                ans, ans_exp = this_best_neuron.perform_calculation_at_data_index(0, True)
                dt = datetime.now()
                finaldf = pd.DataFrame({'rmse':[] ,'equation':[], 'answer':[] ,'answer explanation':[] ,'evolution':[]})
                df_1_deal = pd.DataFrame({'rmse':[this_rmse] ,'equation':[this_best_neuron.describe_neuron()] , 'answer':[ans] ,'answer explanation':[ans_exp] ,'evolution':[evol]})
                finaldf = finaldf.append(df_1_deal)
                finaldf.to_csv((str(dt)+" good_data").replace(".","_").replace(":","_").replace(";","_").replace(",","_")+".csv")
                print("saved")
                print(9/0)
    #    except:
    #        print(" big fail ")


    #mi_neuron = neuron();
    #mi_neuron.describe_neuron()
    #neuron2 = neuron(mi_neuron)

    #    mi_neuron.describe_neuron()

    #neuron2.describe_neuron()
    #ans = mi_neuron.perform_calculation_at_data_index(index =  10)
    #rmse = neuron2.get_rmse()
    #print(rmse)
    #    if ans == all_data[variable_to_calculate][10]:
    #        print(999/0)

#run_function()

if __name__ == "__main__":
        processes = []
        for proce in range(multiprocessing.cpu_count()):
            p1 = Process( target = run_function )
            processes.append(p1)
#
 #
        for proc in processes:
            proc.start()
        for proc in processes:
            proc.join()
