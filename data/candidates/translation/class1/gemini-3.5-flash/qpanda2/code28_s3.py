# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    def get_distribution(state_type):
        machine = pq.CPUQVM()
        machine.init_qvm()
        q = machine.qAlloc_many(2)
        c = machine.cAlloc_many(2)
        
        prog = pq.QProg()
        if state_type == 'phi_plus':
            prog.insert(pq.H(q[0]))
            prog.insert(pq.CNOT(q[0], q[1]))
        elif state_type == 'phi_minus':
            prog.insert(pq.X(q[0]))
            prog.insert(pq.H(q[0]))
            prog.insert(pq.CNOT(q[0], q[1]))
            
        prog.insert(pq.Measure(q[0], c[0]))
        prog.insert(pq.Measure(q[1], c[1]))
        
        shots = 1000
        result = machine.run_with_configuration(prog, c, shots)
        machine.finalize()
        
        total = builtins.sum(result.values())
        return {key: val / total for key, val in result.items()}

    return {
        "phi_plus": get_distribution('phi_plus'),
        "phi_minus": get_distribution('phi_minus')
    }
