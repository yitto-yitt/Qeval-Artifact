# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler

def bell_each_shot():
    backend = AerSimulator()
    cr = ClassicalRegister(2, 'meas')
    qc = QuantumCircuit(2)
    qc.add_register(cr)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], cr)
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    sampler = Sampler(mode=backend)
    result = sampler.run([transpiled_qc], shots=10).result()
    counts = result[0].data.meas.get_counts()
    return {bitstr: count / 10 for bitstr, count in counts.items()}
