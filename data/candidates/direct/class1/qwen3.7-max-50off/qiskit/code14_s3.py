# EVAL_META: task_id=14, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

def bell_each_shot():
    backend = AerSimulator()
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    transpiled_qc = pm.run(qc)
    
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    
    if hasattr(result, 'quasi_dists'):
        quasi = result.quasi_dists[0]
        return {format(k, '02b'): v for k, v in quasi.items()}
    else:
        pub_result = result[0]
        counts = pub_result.data.meas.get_counts()
        total = sum(counts.values())
        return {k: v / total for k, v in counts.items()}
