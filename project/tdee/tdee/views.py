from django.http import HttpResponse
from django.shortcuts import render
from tdee import tdee

def homePage(request):
	return render(request, "form.html")

def welcome(request):
        return render(request, "hello.html")

def receivedata(request):
        if request.method == "POST":
                system_type = request.POST['type']
                spacing_phase1 = int(request.POST['spacingpc1'])
                spacing_phase2= int(request.POST['spacingpc2'])
                spacing_phase3 = int(request.POST['spacingpc3'])
                subconductor = int(request.POST['numberofsc'])
                spacing_subconductor = int(request.POST['spacingsc'])
                strands = int(request.POST['strands'])
                diameter = int(request.POST['diameter'])
                line_length = int(request.POST['lengthkm'])
                line_model = request.POST['model']
                resistance = int(request.POST['resistance'])
                power_frequency = int(request.POST['powerfrequency'])
                nominal_voltage = int(request.POST['nomsysvoltage'])
                receiving_load = int(request.POST['load'])
                power_factor = float(request.POST['pf'])

                if system_type == "Symmetrical":
                        GMD = tdee.find_GMD_sym(spacing_phase1)
                if system_type == "Unsymmetrical":
                        GMD = tdee.find_GMD_asym(spacing_phase1, spacing_phase2, spacing_phase3)
                print(type(diameter))
                print(GMD)
                GMR_inductance = tdee.GMR_inductance(subconductor, diameter, spacing_subconductor)
                GMR_capacitance = tdee.GMR_capacitance(subconductor, diameter, spacing_subconductor)
                print(GMR_inductance)
                inductance = tdee.inductance_per_phase(GMD, GMR_inductance)*10**6
                capacitance = tdee.capacitance_per_phase(GMD,GMR_capacitance )*10**9

                xc = tdee.capacitive_reactance(capacitance)
                xl = tdee.inductive_reactance(inductance)

                charging_current = tdee.charging_current(nominal_voltage, xc)
                ABCD = tdee.ABCD_parameters(line_model, resistance, xl, xc)

                sending_in_voltage, sending_in_current = tdee.sending_in_voltage(receiving_load, nominal_voltage, power_factor, ABCD)

                voltage_regulation = tdee.voltage_regulation(sending_in_voltage, nominal_voltage)*100

                powerLoss = tdee.powerLoss(sending_in_voltage, sending_in_current, receiving_load, nominal_voltage, power_factor)

                efficiency = tdee.efficiency(sending_in_voltage, sending_in_current, receiving_load, nominal_voltage, power_factor)*100


                dict_ = {'inductance':inductance, 'capacitance': capacitance, 'inductivereactance': xl,'capacitivereactance':xc, 'chargingcurrent': charging_current, 'ABCD': ABCD,
                         'sendinginvoltage': sending_in_voltage, 'sendingincurrent': sending_in_current, 'voltageregulation': voltage_regulation, 'powerLoss': powerLoss, 'efficiency': efficiency 
                             }
                return render(request, "parameters.html", dict_)
        else:
                return render(request, "parameters.html")

def lineparameters(request):
        return render(request, "form.html")


