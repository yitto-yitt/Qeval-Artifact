# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, QCircuit, H, X, Measure, QMachine

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'qubit_num'):
        n = oracle.qubit_num
    elif hasattr(oracle, 'qubits'):
        n = len(oracle.qubits)
    else:
        n = len(oracle.get_qubits())
        
    if hasattr(oracle, 'qubits'):
        qubits = list(oracle.qubits)
    else:
        qubits = list(oracle.get_qubits())
        
    machine = QMachine()
    cbits = machine.cAlloc(n - 1)
    
    prog = QProg()
    prog << X(qubits[-1])
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
        
    try:
        probs = machine.get_probabilities(prog)
        if isinstance(probs, dict):
            return {k: v for k, v in probs.items() if v > 1e-12}
    except Exception:
        pass
        
    try:
        probs = machine.get_prob(prog)
        if isinstance(probs, dict):
            return {k: v for k, v in probs.items() if v > 1e-12}
    except Exception:
        pass

    result = machine.run(prog, 1000000)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
