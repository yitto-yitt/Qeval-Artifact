# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def bell_each_shot():
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qubit_alloc(2)
    cbits = machine.cbit_alloc(2)

    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.measure_all(qubits, cbits)

    shots = 10
    counts = machine.run_with_configuration(prog, cbits, shots)

    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    machine.finalize()
    return result
