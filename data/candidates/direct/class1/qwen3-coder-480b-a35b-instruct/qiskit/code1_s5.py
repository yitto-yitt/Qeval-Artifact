# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler


def run_bell_state_simulator():
    # Create a quantum circuit for Phi+ Bell state (|00> + |11>)
    qc = QuantumCircuit(2)
    qc.h(0)  # Apply Hadamard to first qubit
    qc.cx(0, 1)  # Apply CNOT from first to second qubit
    qc.measure_all()  # Measure all qubits

    # Transpile the circuit using a preset pass manager at optimization level 1
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)

    # Run the transpiled circuit using Qiskit Runtime Sampler
    sampler = Sampler(backend=backend)
    result = sampler.run(transpiled_circuit).result()

    # Extract the probability distribution
    quasi_dist = result.quasi_dists[0]
    # Convert quasi distribution to regular probability distribution
    prob_dist = {}
    for key, value in quasi_dist.items():
        # Convert integer key to binary string with proper padding
        bin_str = format(key, f'0{transpiled_circuit.num_clbits}b')
        prob_dist[bin_str] = value

    return prob_dist
