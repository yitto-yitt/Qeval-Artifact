# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2


def init_random_3qubit(desired_vector):
    backend = AerSimulator()
    sampler = SamplerV2(backend)

    qc = QuantumCircuit(3)
    qc.append(StatePreparation(desired_vector), [0, 1, 2])
    qc.measure_all()

    job = sampler.run([qc], shots=1024)
    result = job.result()

    counts = result[0].data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
