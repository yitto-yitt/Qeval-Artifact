# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    isa_circuit = pm.run(qc)
    sampler = Sampler(backend=backend)
    job = sampler.run([isa_circuit], shots=10)
    result = job.result()
    counts = result[0].data.meas.get_counts()
    shots = 10
    return {k: v / shots for k, v in counts.items()}
