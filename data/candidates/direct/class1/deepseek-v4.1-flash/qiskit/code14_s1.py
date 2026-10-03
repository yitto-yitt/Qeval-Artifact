# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()

    backend = AerSimulator(seed_simulator=1234)
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    probabilities = {key: val / 10 for key, val in counts.items()}
    return probabilities
