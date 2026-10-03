# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit.primitives import Sampler


def bell_each_shot():
    # Create a Phi+ Bell state circuit
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    # Get the Aer simulator backend
    backend = AerSimulator()

    # Transpile the circuit with optimization level 1
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pm.run(qc)

    # Use the Sampler primitive to run the circuit
    sampler = Sampler(backend=backend)
    result = sampler.run([transpiled_circuit], shots=10).result()
    
    # Extract the probability distribution
    pub_result = result.pub_results[0]
    counts = pub_result.data.c.get_counts()
    
    # Convert counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return prob_dist
