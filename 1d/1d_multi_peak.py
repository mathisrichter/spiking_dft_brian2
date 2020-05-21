from brian2 import *
from brian2tools import *
import matplotlib

N = 120
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
refractory_period = 2.0*ms # should be 2.0*ms

eqs = '''
    dv/dt = (-v + v_rest)/time_scale: volt (unless refractory)
    '''

# 1D neural field
G = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G.v = v_rest

exc = 5.0
inh = 4.2
width = 15.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='v+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh * exp(-(i-j)**2/(2*((2 * width)**2)))) * mV'


# 1D neural field without interaction
# (this is only used to show the effect of recurrent connections)
G1 = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G1.v = v_rest


# input
input_center1 = 28.0
input_center2 = 100.0
input_strength = 2000.0
PG = PoissonGroup(N, 'input_strength * (exp(-(input_center1-i)**2/(2*6.0**2)) + exp(-(input_center2-i)**2/(2*6.0**2)))* Hz')
SP = Synapses(PG, G, on_pre='v+=1.0 * mV')
SP.connect(j='i')
SP1 = Synapses(PG, G1, on_pre='v+=1.0 * mV')
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

run(runtime/2.)
input_strength = 0.0
run(runtime/2.)


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
suptitle('Spikes of the field (without interaction)')
plot(M1.t/ms, M1.i, '.r')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
suptitle('Spike rate of the field with interaction (black) and without (red)')
plot(MR.t/ms, MR.smooth_rate(width=50*ms), 'k')
plot(MR1.t/ms, MR1.smooth_rate(width=50*ms), 'r')
xlabel('Time (ms)')
ylabel('Firing rate (spikes/s)')
legend()

figure()
suptitle('Membrane potential of all field neurons (with interaction)')
brian_plot(MS)

figure()
suptitle('Kernel of the field (with interaction)')
brian_plot(S.w)
show()
