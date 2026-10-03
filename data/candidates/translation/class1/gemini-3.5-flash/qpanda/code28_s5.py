# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # phi_plus
    prog_plus = pq.QProg()
    prog_plus << pq.H(qubits[0])
    prog_plus << pq.CNOT(qubits[0], qubits[1])
    prog_plus << pq.Measure(qubits[0], cbits[0])
    prog_plus << pq.Measure(qubits[1], cbits[1])
    
    result_plus = machine.run_with_configuration(prog_plus, cbits, 1000)
    
    # phi_minus
    prog_minus = pq.QProg()
    prog_minus << pq.X(qubits[0])
    prog_minus << pq.H(qubits[0])
    prog_minus << pq.CNOT(qubits[0], qubits[1])
    prog_minus << pq.Measure(qubits[0], cbits[0])
    prog_minus << pq.Measure(qubits[1], cbits[1])
    
    result_minus = machine.run_with_configuration(prog_minus, cbits, 1000)
    
    machine.finalize()
    
    phi_plus_total = sum(result_plus.values())
    phi_minus_total = sum(result_minus.values())
    
    return {
        "phi_plus": {key: value / phi_plus_total for key, value in result_plus.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in result_minus.items()},
    }
