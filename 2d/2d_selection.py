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

# 2D field
G = NeuronGroup(neurons_per_dimension**2, eqs, threshold='v>firing_threshold', reset=reset_eqs, refractory=refractory_period, method='exact')
G.v = v_rest
G.s = 0.0 * mV

exc = 10.0
inh = 9.0
width = 40.0

S = Synapses(G, G, 'w : volt', delay=3*ms, on_pre='s+=w')
S.connect()
S.w = '(exc * exp(-(i-j)**2/(2*(width**2))) - inh) * mV'


# input
input_center_x = 30.0
input_center_y = 30.0
input_strength = 2000.0

#PG = PoissonGroup(N*N, 'input_strength * (exp(-(input_center_x-(i % neurons_per_dimension))**2/(2*2.0**2)) * exp(-(input_center_y-(i//N))**2/(2*2.0**2)))* Hz') # the % operator is modulo; the // operator is floor division
PG = PoissonGroup(neurons_per_dimension**2, 'input_strength * exp(-(input_center_x-(i % neurons_per_dimension))**2/(2*2.0**2)) * exp(-(input_center_y - (i//neurons_per_dimension))**2/(2*2.0**2)) * Hz') # the % operator is modulo; the // operator is floor division
SP = Synapses(PG, G, on_pre='s+=1.0 * mV')
SP.connect(j='i')


# monitors
MP = SpikeMonitor(PG)
M = SpikeMonitor(G)
MS = StateMonitor(G, variables='v', record=True)

net = Network(collect())  # automatically include the above monitors

#pop_rate_monitors = [ PopulationRateMonitor(G[n]) for n in range(0, G.N) ]
#net.add(pop_rate_monitors) # manually add these monitors (they are not automatically added because they are in a list




# simulation
runtime = 2*second

net.run(runtime/2.)
input_strength = 0.0
net.run(runtime/2.)



# projecting spikes
number_of_spikes = len(M.i)
x_indices = np.zeros(number_of_spikes)
y_indices = np.zeros(number_of_spikes)

for i, index in enumerate(M.i):
    x_indices[i] = index % neurons_per_dimension # neurons per dimension x
    y_indices[i] = index // neurons_per_dimension # neurons per dimension y


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

# x
figure()
plot(M.t/ms, x_indices, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
grid()
#yticks(numpy.arange(0, neurons_per_dimension**2, neurons_per_dimension))
xlim(0,runtime/ms)
ylim(0,neurons_per_dimension)

# y
figure()
plot(M.t/ms, y_indices, '.k')
xlabel('Time (ms)')
ylabel('Neuron index')
grid()
#yticks(numpy.arange(0, neurons_per_dimension**2, neurons_per_dimension))
xlim(0,runtime/ms)
ylim(0,neurons_per_dimension)


#figure()
#suptitle('Spike rate of the field (Hz)')
#pop_spikerates = np.vstack([np.array(monitor.smooth_rate(width=50*ms)) for monitor in pop_rate_monitors])
#im = pcolormesh(pop_spikerates)
#colorbar(im)
#xlabel('Time (ms)')
#ylabel('Neuron index')
#legend()


figure()
brian_plot(MS)

figure()
brian_plot(S.w)
show()
