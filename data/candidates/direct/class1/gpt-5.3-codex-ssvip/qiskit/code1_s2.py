# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


def run_bell_state_simulator():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    tqc = pm.run(qc)

    sampler = Sampler(mode=backend)
    job = sampler.run([tqc], shots=4096)
    result = job.result()

    pub_result = result[0]
    data_bin = pub_result.data.c
    counts = data_bin.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
