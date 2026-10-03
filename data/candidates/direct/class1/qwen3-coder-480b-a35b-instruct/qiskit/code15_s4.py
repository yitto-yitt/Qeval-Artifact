# EVAL_META: task_id=15, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer.noise import NoiseModel
from qiskit_aer import AerSimulator
from qiskit.providers.fake_provider import FakeVigo
from qiskit.primitives import Sampler


def noisy_bell():
    # Create a simple Bell circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Get a fake backend to create noise model
    fake_backend = FakeVigo()
    
    # Create a noisy simulator based on the fake backend
    noise_model = NoiseModel.from_backend(fake_backend)
    coupling_map = fake_backend.configuration().coupling_map
    basis_gates = fake_backend.configuration().basis_gates
    
    simulator = AerSimulator(
        noise_model=noise_model,
        coupling_map=coupling_map,
        basis_gates=basis_gates
    )
    
    # Generate a preset pass manager at optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, target=simulator.target)
    
    # Transpile the circuit using the pass manager
    transpiled_circuit = pm.run(qc)
    
    # Use the Sampler primitive to execute the circuit
    sampler = Sampler(backend=simulator)
    result = sampler.run(transpiled_circuit).result()
    
    # Convert the result to a probability distribution dictionary
    # The result contains quasi-probabilities; convert them to probabilities
    quasi_dist = result.quasi_dists[0]
    prob_dist = {}
    for key, value in quasi_dist.items():
        # Convert integer key to binary string with proper width
        bitstring = format(key, f'0{transpiled_circuit.num_clbits}b')
        prob_dist[bitstring] = value
        
    return prob_dist
