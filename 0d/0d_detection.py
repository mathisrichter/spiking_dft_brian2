from brian2 import *
from brian2tools import *
import matplotlib

N = 38 # one more and you get self-sustained activation
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
time_scale_input = 10.0*ms
refractory_period = 2.0*ms


# 0-dimensional neural node
eqs = '''
    dv/dt = (-v + v_rest + s)/time_scale : volt (unless refractory)
    ds/dt = -s/time_scale_input : volt
    '''

reset_eqs = '''
    v -= (firing_threshold - v_reset)
    s = 0.0 * mV
    '''
G = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset=reset_eqs, refractory=refractory_period, method='exact')
G.v = v_rest

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='s += 1.0 * mV')
S.connect(condition='j!=i')


# 0-dimensional neural node (without self-excitation)
G1 = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset=reset_eqs, refractory=refractory_period, method='exact')
G1.v = v_rest


# input
input_strength = 500.0
PG = PoissonGroup(N, 'input_strength * Hz')
SP = Synapses(PG, G, on_pre='s+=1.0*mV')
SP.connect(j='i')
SP1 = Synapses(PG, G1, on_pre='s+=1.0*mV')
SP1.connect(j='i')


# monitors
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
M1 = SpikeMonitor(G1)
MS = StateMonitor(G, variables='v', record=True)
MR = PopulationRateMonitor(G)
MR1 = PopulationRateMonitor(G1)


# simulation
runtime = 2*second

input_strength = 500.
run(runtime/8.)
input_strength = 1000.
run(runtime/8.)
input_strength = 1500.
run(runtime/8.)
input_strength = 2000.
run(runtime/8.)
input_strength = 1500.
run(runtime/8.)
input_strength = 1000.
run(runtime/8.)
input_strength = 500.
run(runtime/8.)
input_strength = 0.
run(runtime/8.)


# plotting
figure()
suptitle('Poisson input to the node')
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Spikes of the neurons of the node (with interaction)')
plot(M.t/ms, M.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Spikes of the neurons of the node (without interaction)')
plot(M1.t/ms, M1.i, '.r')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Membrane potential of all neurons of the node (with interaction)')
brian_plot(MS)

figure()
suptitle('Average population spike rate with interaction (black) and without (red)')
plot(MR.t/ms, MR.smooth_rate(width=50*ms), 'k')
plot(MR1.t/ms, MR1.smooth_rate(width=50*ms), 'r')
xlabel('Time (ms)')
ylabel('Firing rate (spikes/s)')
legend()

show()
