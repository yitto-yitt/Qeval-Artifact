# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def run_bell_state_simulator():
    # Create a quantum circuit for Phi+ Bell state (|00> + |11>)
    qc = QuantumCircuit(2)
    qc.h(0)  # Apply Hadamard to first qubit
    qc.cx(0, 1)  # Apply CNOT with qubit 0 as control and qubit 1 as target
    qc.measure_all()

    # Transpile the circuit with optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)

    # Run the circuit using Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    result = sampler.run(transpiled_circuit).result()

    # Extract the probability distribution
    quasi_dist = result.quasi_dists[0]
    # Convert to bitstring probabilities
    prob_dist = {}
    for outcome, prob in quasi_dist.items():
        # Format outcome as bitstring
        bitstring = format(outcome, f'0{transpiled_circuit.num_clbits}b')
        prob_dist[bitstring] = prob

    return prob_dist
