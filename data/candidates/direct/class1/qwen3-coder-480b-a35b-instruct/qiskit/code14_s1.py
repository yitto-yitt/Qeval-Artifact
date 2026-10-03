# EVAL_META: task_id=14, framework=qiskit, class=1

from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit_aer import AerSimulator

def bell_each_shot():
    # Create Phi+ Bell state circuit
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    # Get backend and generate pass manager
    backend = AerSimulator()
    pm = generate_preset_pass_manager(optimization_level=1, backend=backend)
    
    # Transpile circuit
    transpiled_qc = pm.run(qc)
    
    # Run with Sampler
    service = QiskitRuntimeService()
    sampler = Sampler(backend=backend)
    job = sampler.run([transpiled_qc], shots=10)
    result = job.result()
    
    # Extract and return probability distribution
    quasi_dist = result.quasi_dists[0]
    return {format(k, f'0{len(qc.clbits)}b'): v for k, v in quasi_dist.items()}
