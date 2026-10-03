# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Determine the number of qubits from the circuit
    used_qubits = []
    if hasattr(circuit, 'get_used_qubits'):
        used_qubits = circuit.get_used_qubits()
    elif hasattr(circuit, 'get_qubits'):
        used_qubits = circuit.get_qubits()
    
    if used_qubits:
        max_index = max(q.get_phys_addr() for q in used_qubits)
        n = max_index + 1
    else:
        n = 0
    
    if n > 0:
        qvm.qAlloc_many(n)
    
    prog = QProg()
    if isinstance(circuit, QProg):
        prog = circuit
    else:
        prog << circuit
    
    qvm.run(prog)
    state = qvm.get_qstate()
    qvm.finalize()
    return state
