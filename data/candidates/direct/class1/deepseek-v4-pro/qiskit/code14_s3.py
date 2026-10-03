# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def bell_each_shot():
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_circuit = pass_manager.run(circuit)

    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_circuit], shots=10)
    result = job.result()
    quasi_dist = result.quasi_dists[0]

    return {
        key if isinstance(key, str) else format(int(key), f"0{transpiled_circuit.num_clbits}b"): value
        for key, value in quasi_dist.items()
    }
