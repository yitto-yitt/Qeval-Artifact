# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2
def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    sampler = SamplerV2(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    shots = 10
    prob_dist = {k: v / shots for k, v in counts.items()}
    return prob_dist
