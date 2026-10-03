# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def bell_each_shot():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    sampler = SamplerV2(mode=backend)
    job = sampler.run([isa_circuit], shots=10)
    result = job.result()
    counts = result[0].data.c.get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
