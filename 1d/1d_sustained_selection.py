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
G = NeuronGroup(N, eqs, threshold='v>firing_threshold', reset='v=v_reset', refractory=refractory_period, method='exact')
G.v = v_rest


exc = 15.0
inh = 13.0
width = 40.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='v+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh) * mV'

input_center1 = 28.0
input_center2 = 100.0
input_strength = 2000.0
PG = PoissonGroup(N, 'input_strength * (exp(-(input_center1-i)**2/(2*6.0**2)) + exp(-(input_center2-i)**2/(2*6.0**2)))* Hz')
SP = Synapses(PG, G, on_pre='v+=1.0 * mV')
SP.connect(j='i')
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)

runtime = 2*second

run(runtime/2.)
input_strength = 0.0
run(runtime/2.)

figure()
plot(MP.t/ms, MP.i, '.k')
xlabel('Time (ms)')
ylabel('Input index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
plot(M.t/ms, M.i, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
xlim(0,runtime/ms)
ylim(0,N)

figure()
brian_plot(MS)

figure()
brian_plot(S.w)
show()
