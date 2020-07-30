from brian2 import *
from brian2tools import *
import matplotlib

# parameters
N0 = 15
N1 = 120
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
refractory_period = 2.0*ms

eqs = '''
    dv/dt = (-v + v_rest)/time_scale: volt (unless refractory)
    '''

# 0D field / node
G0 = NeuronGroup(N0, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G0.v = v_rest

S00 = Synapses(G0, G0, 'w : volt', delay=3*ms, on_pre='v+=w')
S00.connect(condition='j!=i')
S00.w = 1.0*mV


# 1D field
G1 = NeuronGroup(N1, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G1.v = v_rest

exc = 5.0
inh = 4.2
width = 15.0

S11 = Synapses(G1, G1, 'w : volt', delay=3*ms, on_pre='v+=w')
S11.connect()
S11.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh * exp(-(i-j)**2/(2*((2 * width)**2)))) * mV'


# coupling
S10 = Synapses(G0, G1, 'w : volt', delay=3*ms, on_pre='v+=w')
S10.connect()
s10_center = 60
S10.w = '(2.0 * exp(-(s10_center-j)**2/(2*(15.0**2)))) * mV'


# input
input_strength = 2000.0
P = PoissonGroup(N0, 'input_strength * Hz')
S0P = Synapses(P, G0, on_pre='v+=1.0 * mV')
S0P.connect(j='i')


# monitors
MP = SpikeMonitor(P)
M0 = SpikeMonitor(G0)
M1 = SpikeMonitor(G1)
MS0 = StateMonitor(G0, variables='v', record=True)
MS1 = StateMonitor(G1, variables='v', record=True)


# simulation
runtime = 2*second
run(runtime)


# plotting
figure()
suptitle('Poisson input into node')
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
xlim(0,runtime/ms)
ylim(0,N0)

figure()
suptitle('Spikes of node')
plot(M0.t/ms, M0.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N0)

figure()
suptitle('Spikes of 1D field')
plot(M1.t/ms, M1.i, '.r')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N1)

figure()
suptitle('Membrane potential of all node neurons')
brian_plot(MS0)

figure()
suptitle('Membrane potential of all field neurons')
brian_plot(MS1)

figure()
suptitle('Connection weights from node to field')
brian_plot(S10.w)
show()
