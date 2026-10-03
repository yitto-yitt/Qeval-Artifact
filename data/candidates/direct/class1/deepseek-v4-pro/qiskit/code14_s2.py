# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2


def bell_each_shot():
    qr = QuantumRegister(2, 'q')
    cr = ClassicalRegister(2, 'meas')
    qc = QuantumCircuit(qr, cr)
    qc.h(qr[0])
    qc.cx(qr[0], qr[1])
    qc.measure(qr, cr)

    backend = AerSimulator()

    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)

    sampler = SamplerV2(backend=backend)
    job = sampler.run([isa_circuit], shots=10)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total_shots = sum(counts.values())
    return {bits: count / total_shots for bits, count in counts.items()}
