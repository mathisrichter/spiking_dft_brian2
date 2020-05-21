from brian2 import *
from brian2tools import *
import matplotlib

N = 20
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

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='v+=w')
S.connect(condition='j!=i')
S.w = 1.0*mV

input_strength = 1200.0
PG = PoissonGroup(N, 'input_strength * Hz')
indices = array([0])
times = array([0.0]) * ms
SP = Synapses(PG, G, on_pre='v+=1.0*mV')
SP.connect(j='i')
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)
MR = PopulationRateMonitor(G)

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
plot(MR.t/ms, MR.smooth_rate(width=50*ms))
xlabel('Time (ms)')
ylabel('Firing rate (spikes/s)')

#figure()
#brian_plot(S.w)
show()
