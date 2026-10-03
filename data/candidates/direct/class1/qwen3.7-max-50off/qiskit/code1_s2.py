# EVAL_META: task_id=1, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler

def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    backend = AerSimulator()
    qc_transpiled = transpile(qc, backend, optimization_level=1)
    
    sampler = Sampler(mode=backend)
    job = sampler.run([qc_transpiled], shots=1024)
    result = job.result()
    
    pub_result = result[0]
    counts = pub_result.data.meas.get_counts()
    
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}
    return probs
