# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda
import builtins

def init_random_3qubit(desired_vector):
    qvm = pyqpanda.init_quantum_machine(pyqpanda.QMachineType.CPU)
    qubits = qvm.qAlloc_many(3)
    
    prog = pyqpanda.QProg()
    prog << pyqpanda.init_state(qubits, desired_vector)
    prog << pyqpanda.measure_all(qubits)
    
    counts = qvm.run_with_configuration(prog, {"shots": 10000})
    total = builtins.sum(counts.values())
    
    return {key: value / total for key, value in counts.items()}
