from brian2 import *
from brian2tools import *
import matplotlib

N = 120
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
time_scale_input = 10.0*ms
refractory_period = 2.0*ms

eqs = '''
    dv/dt = (-v + v_rest + s)/time_scale: volt (unless refractory)
    ds/dt = -s/time_scale_input : volt
    '''

reset_eqs = '''
    v -= (firing_threshold - v_reset)
    s = 0.0 * mV
    '''

# 1D neural field
G = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset=reset_eqs, refractory=refractory_period, method='exact')
G.v = v_rest
G.s = 0.0 * mV

exc = 10.2
inh = 9.0
width = 40.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='s+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh) * mV'


# input
input_center1 = 28.0
input_center2 = 100.0
input_strength1 = 2000.0
input_strength2 = 2000.0
PG = PoissonGroup(N, '(input_strength1 * exp(-(input_center1-i)**2/(2*6.0**2)) + input_strength2 * exp(-(input_center2-i)**2/(2*6.0**2)))* Hz')
SP = Synapses(PG, G, on_pre='s+=1.0 * mV')
SP.connect(j='i')


# monitors
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)


# simulation
runtime = 2*second

run(runtime/5.)
input_strength1 = 0.0
run(runtime/5.)
input_strength1 = 2000.0
run(runtime/5.)
input_strength2 = 0.0
run(runtime/5.)
input_strength2 = 2000.0
run(runtime/5.)


# plotting
figure()
suptitle('Poisson input to the field')
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Spikes of the field')
plot(M.t/ms, M.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Membrane potential of all field neurons')
brian_plot(MS)

figure()
suptitle('Kernel of the field')
brian_plot(S.w)
show()
