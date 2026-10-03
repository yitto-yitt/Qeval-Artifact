# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda import *
from typing import Dict

def sampler_qiskit() -> Dict[str, float]:
    qvm = CPUQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(measure_all(qubits, cbits))
    
    result = qvm.run_with_configuration(prog, cbits, 1024)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
