# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, OriginQuantumMachine

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'qubits'):
        n = len(oracle.qubits)
    elif hasattr(oracle, 'qubit_num'):
        n = oracle.qubit_num
    else:
        n = 3

    qc = QuantumCircuit(n)
    qc.x(n - 1)
    for i in range(n):
        qc.h(i)
        
    if callable(oracle):
        oracle_inst = oracle(qc.qubits)
        if hasattr(qc, 'append'):
            qc.append(oracle_inst)
        else:
            qc << oracle_inst
    else:
        if hasattr(qc, 'compose'):
            qc.compose(oracle, inplace=True)
        elif hasattr(qc, 'append'):
            qc.append(oracle)
        else:
            qc << oracle
            
    for i in range(n):
        qc.h(i)
        
    c = []
    for i in range(n - 1):
        c.append(qc.measure(i))
        
    machine = OriginQuantumMachine()
    cbits = qc.cbits if hasattr(qc, 'cbits') else c
    
    try:
        result = machine.run_with_configuration(qc, cbits, 10000)
    except Exception:
        prog = qc.to_prog() if hasattr(qc, 'to_prog') else qc
        result = machine.run_with_configuration(prog, cbits, 10000)
        
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
