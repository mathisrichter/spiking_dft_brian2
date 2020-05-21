#########
# NOT YET WORKING
###


from brian2 import *
from brian2tools import *
import matplotlib

neurons_per_dimension = 40
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
refractory_period = 2.0*ms

eqs = '''
    dv/dt = (-v + v_rest)/time_scale: volt (unless refractory)
    '''

# 2D field
G = NeuronGroup(neurons_per_dimension**2, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G.v = v_rest

exc = 10.0
inh = 9.0
width = 40.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='v+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh) * mV'


# input
input_center_x = 30.0
input_center_y = 30.0
input_strength = 2000.0

#PG = PoissonGroup(N*N, 'input_strength * (exp(-(input_center_x-(i % neurons_per_dimension))**2/(2*2.0**2)) * exp(-(input_center_y-(i//N))**2/(2*2.0**2)))* Hz') # the % operator is modulo; the // operator is floor division
PG = PoissonGroup(neurons_per_dimension**2, 'input_strength * exp(-(input_center_x-(i % neurons_per_dimension))**2/(2*2.0**2)) * exp(-(input_center_y - (i//neurons_per_dimension))**2/(2*2.0**2)) * Hz') # the % operator is modulo; the // operator is floor division
SP = Synapses(PG, G, on_pre='v+=1.0 * mV')
SP.connect(j='i')
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)


# simulation
runtime = 2*second

run(runtime/2.)
input_strength = 0.0
run(runtime/2.)


# plotting
figure()
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
grid()
yticks(numpy.arange(0, neurons_per_dimension**2, neurons_per_dimension))
xlim(0,runtime/ms)
ylim(0,neurons_per_dimension**2)

figure()
plot(M.t/ms, M.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
grid()
yticks(numpy.arange(0, neurons_per_dimension**2, neurons_per_dimension))
xlim(0,runtime/ms)
ylim(0,neurons_per_dimension**2)

figure()
brian_plot(MS)

figure()
brian_plot(S.w)
show()
