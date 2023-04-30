import math
import numpy as np
import cmath

e0=8.85*10**-12
math.log(math.e)

#gmr


#gmd
#symetrical
#in metres
def find_GMD_sym(spacing_phase):
    gmd_sym=spacing_phase
    return gmd_sym
#unsymetrical

def find_GMD_asym(d1,d2,d3):
    gmd_uns=(d1*d2*d3)^(1/3)
    return gmd_uns

def GMR_inductance(n, diameter, spacing_subconductor):
    r=0.7788*diameter/2
    if n==1:
        return r
    if n==2:
        rr = math.sqrt(r*spacing_subconductor)
        return rr
    if n==3:
        rr = math.pow(r*spacing_subconductor**2, 1/3)
        return rr
    if n==4:
        rr = math.pow(r*2*math.sqrt(2)*spacing_subconductor**3, 1/4)
        return rr
    
def GMR_capacitance(n, diameter, spacing_subconductor):
    r=diameter/2
    if n==1:
        return r
    if n==2:
        rr = math.sqrt(r*spacing_subconductor)
        return rr
    if n==3:
        rr = math.pow(r*spacing_subconductor**2, 1/3)
        return rr
    if n==4:
        rr = math.pow(r*2*math.sqrt(2)*spacing_subconductor**3, 1/4)
        return rr

def inductance_per_phase(GMD, GMR):
    t2=math.log(GMD/GMR)
    ls= 2*10**-7*t2
    return ls

def capacitance_per_phase(GMD,GMR):
    t2=math.log(GMD/GMR)
    cs=2*3.14*e0/t2
    return cs
    
def capacitive_reactance(cs):
    xc= 1/(2*math.pi*50*cs)
    return xc

def inductive_reactance(ls):
    xl= 2*math.pi*50*ls
    return xl

def charging_current(nominal_voltage, xc):
    nominal_voltage = nominal_voltage*10**3
    ch_i=nominal_voltage/(xc*math.sqrt(3)) 
    return ch_i

def ABCD_parameters(line_model, resistance, xl, xc):
    z=complex(resistance,xl)
    if line_model == "Short":
        a_s=1
        b_s=z
        c_s=0
        d_s=1
        return [[a_s, b_s],[c_s, d_s]]
    else:
        y= 0+1j/xc
        a_pi=1+(z*y/2)
        b_pi=z
        c_pi=y+(z*y*y/4)
        d_pi=1+(z*y/2) 
        return [[a_pi, b_pi], [c_pi, d_pi]]
    
def sending_in_voltage(receiving_load, nominal_voltage, power_factor, ABCD):
    #nominal_voltage = nominal_voltage*10**3
    #receiving_load = receiving_load*10**6
    receiving_current= receiving_load/(1.73*nominal_voltage*power_factor)
    receiving_current_rad= math.acos(.9)
    receiving_current_deg=receiving_current_rad*( 180/3.14 )*(-1)
    receiving_current_full=complex(receiving_current*(math.cos(receiving_current_rad)),receiving_current*(math.sin(receiving_current_rad)))
    a = ABCD[0][0]
    b = ABCD[0][1]
    c = ABCD[1][0]
    d = ABCD[1][1]
    v_sending= (a*nominal_voltage/math.sqrt(3)) + (b*receiving_current_full)
    #v_sending= abs(v_sending)
    #nominal pi #sending end current
    i_sending= (c*nominal_voltage/math.sqrt(3)) + (d*receiving_current_full)

    return v_sending, i_sending

def voltage_regulation(v_sending, nominal_voltage):
    #nominal_voltage = nominal_voltage*10**3
    voltage_regulation = (abs(v_sending) - (nominal_voltage/math.sqrt(3)))/(nominal_voltage/math.sqrt(3))
    return voltage_regulation

def powerLoss(v_sending, i_sending, receiving_load, nominal_voltage, power_factor):
    #nominal_voltage = nominal_voltage*10**3
    #receiving_load = receiving_load*10**6
    i_receiving = receiving_load/(1.73*nominal_voltage*power_factor)
    loss = (abs(v_sending)*abs(i_sending)*math.cos(cmath.phase(v_sending/i_sending))- nominal_voltage*abs(i_receiving)*math.cos(cmath.phase(nominal_voltage/i_receiving))/(math.sqrt(3)) )
    return loss

def efficiency(v_sending,i_sending, receiving_load, nominal_voltage, power_factor):
    #receiving_load = receiving_load*10**6
    #nominal_voltage = nominal_voltage*10**3
    i_receiving = receiving_load/(1.73*nominal_voltage*power_factor)
    n=(nominal_voltage*abs(i_receiving)*math.cos(cmath.phase(nominal_voltage/i_receiving))/(math.sqrt(3)))/abs(v_sending)*abs(i_sending)*math.cos(cmath.phase(v_sending/i_sending))
    return n







#c.reactance

#i.reactance

#charging current

#parameters

#nominal pi(put an or loop make abcd same variable)




#short line

#nominal pi


#Vs= AVR + BIR
#nominal pi #sending end voltages in kV

                              


                               
#voltage regulation
#vs/a -vr/vr


#power loss
# Ps = 3 × 63.12 × 307.584 cos (11.670 + 32.8160) × 10 = 41.552 MW
#angle_sending=math.cos()
#power_sending= 3* 


#efficiency


if __name__ == "__main__":
    system_type= input("Symmetrical or Unsymmetrical")
    spacing_phase= int(input("spacing"))
    subconductor=int(input("Number of subconductors per bundle"))
    spacing_subconductor = int(input("Spacing between Subconductors"))
    strands= int(input("strands"))
    diameter= int(input("diameter of each strand"))
    line_length=int(input("length of line in meters"))
    line_model= input("short/nominal pi")
    resistance=int(input("resistance per km"))
    power_frequency=int(input("power frequency"))
    nominal_voltage= int(input("nominal system voltage"))
    receiving_load= int(input("receiving end load in MW"))
    power_factor= int(input("power factor of receiving end load"))
