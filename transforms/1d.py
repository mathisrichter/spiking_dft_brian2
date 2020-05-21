#########
# NOT YET WORKING
###


from brian2 import *
from brian2tools import *
import matplotlib

# parameters
N0 = 120
N1 = 120
v_rest = -70*mV
v_reset = v_rest
firing_threshold = -55*mV
time_scale = 8.0*ms
refractory_period = 2.0*ms

eqs = '''
    dv/dt = (-v + v_rest)/time_scale: volt (unless refractory)
    '''

# 1D reference field
G0 = NeuronGroup(N0, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G0.v = v_rest

exc = 5.0
inh = 4.2
width = 15.0
1d_kernel = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh * exp(-(i-j)**2/(2*((2 * width)**2)))) * mV'

S00 = Synapses(G0, G0, 'w : volt', delay=3*ms, on_pre='v+=w')
S00.connect()
S00.w = 1d_kernel


# 1D target field
G1 = NeuronGroup(N0, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G1.v = v_rest

S11 = Synapses(G1, G1, 'w : volt', delay=3*ms, on_pre='v+=w')
S11.connect()
S11.w = 1d_kernel


# 2D transformation field
G2 = NeuronGroup(N0*N0, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G2.v = v_rest

# keep it input-driven for now
#S22 = Synapses(G2, G2, 'w : volt', delay=3*ms, on_pre='v+=w')
#S22.connect()
#S22.w = 2d_kernel


# 1D relational field
G3 = NeuronGroup(N1, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G3.v = v_rest

S33 = Synapses(G3, G3, 'w : volt', delay=3*ms, on_pre='v+=w')
S33.connect()
S33.w = kernel


# coupling
S10 = Synapses(G0, G1, 'w : volt', delay=3*ms, on_pre='v+=w')
S10.connect()
coupling_strength = 2.5
coupling_width = 5.0
S10.w = 'coupling_strength * exp(-(i-j)**2/(2*(coupling_width**2))) * mV'


# input
input_center = 20.0
input_strength = 2000.0
P = PoissonGroup(N0, '(input_strength * exp(-(input_center-i)**2/(2*(6.0**2))))* Hz')
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

for t in range(16):
    input_center += 5.0
    run(runtime/16.)


# plotting
figure()
suptitle('Poisson input into field0')
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
xlim(0,runtime/ms)
ylim(0,N1)

figure()
suptitle('Spikes of field0')
plot(M0.t/ms, M0.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N0)

figure()
suptitle('Spikes of field1')
plot(M1.t/ms, M1.i, '.r')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N1)

figure()
suptitle('Membrane potential of all field0 neurons')
brian_plot(MS0)

figure()
suptitle('Membrane potential of all field1 neurons')
brian_plot(MS1)

figure()
suptitle('Connection weights from field0 to field1')
brian_plot(S10.w)
show()
