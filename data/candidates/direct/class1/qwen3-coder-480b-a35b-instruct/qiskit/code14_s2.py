# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler


def bell_each_shot():
    # Create a Phi+ Bell state circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.x(1)  # Initialize qubit 1 to |1>
    qc.cx(0, 1)  # Create entanglement
    qc.measure([0, 1], [0, 1])

    # Transpile the circuit with optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)

    # Use Sampler primitive to run the circuit
    sampler = Sampler(backend=backend)
    result = sampler.run([transpiled_circuit], shots=10).result()

    # Extract the probability distribution
    quasi_dist = result.quasi_dists[0]
    
    # Convert to probability distribution dictionary with bitstrings
    prob_dist = {}
    for outcome, prob in quasi_dist.items():
        # Convert integer outcome to binary string with proper width (2 bits)
        bitstring = format(outcome, '02b')
        prob_dist[bitstring] = prob
    
    return prob_dist
