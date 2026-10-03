# EVAL_META: task_id=40, framework=qiskit, class=1
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import StatePreparation
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def init_random_3qubit(desired_vector):
    qr = QuantumRegister(3, 'q')
    cr = ClassicalRegister(3, 'meas')
    qc = QuantumCircuit(qr, cr)
    qc.append(StatePreparation(desired_vector), qr)
    qc.measure(qr, cr)

    backend = AerSimulator()
    sampler = Sampler(backend=backend)
    job = sampler.run([qc], shots=4096)
    result = job.result()
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
