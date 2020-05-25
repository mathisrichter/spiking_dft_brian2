from brian2 import *
from brian2tools import *
import matplotlib

N = 120
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
time_scale_input = 10.0*ms
refractory_period = 2.0*ms # should be 2.0*ms

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

exc = 15.5
inh = 13.0
width = 40.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='s+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh) * mV'


# input
input_center = 28.0
input_strength = 2000.0
PG = PoissonGroup(N, 'input_strength * (exp(-(input_center-i)**2/(2*6.0**2)))* Hz')
SP = Synapses(PG, G, on_pre='s+=1.0 * mV')
SP.connect(j='i')


# monitors
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)


# simulation
runtime = 2*second

run(runtime/8.)
input_strength = 0.
run(runtime/8.)
input_strength = 1600.
for _ in range(12):
    input_center += 5.0
    run(runtime/16.)


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
