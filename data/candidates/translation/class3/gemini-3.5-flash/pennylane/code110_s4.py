# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import random

def equivalent_clifford_circuit(circuit, n):
    try:
        tape = qml.workflow.construct_tape(circuit)()
    except Exception:
        try:
            tape = qml.tape.make_qscript(circuit)()
        except Exception:
            with qml.queuing.AnnotatedQueue() as q:
                circuit()
            tape = qml.tape.QuantumScript.from_queue(q)
            
    ops = tape.operations
    wires = list(tape.wires) if len(tape.wires) > 0 else [0]
    
    qc_list = []
    for _ in range(n):
        def make_func(ops_list=ops, w_list=wires):
            def new_circuit():
                for op in ops_list:
                    if random.random() < 0.3:
                        wire = random.choice(w_list)
                        id_type = random.choice(['HH', 'SSSS', 'XX', 'ZZ', 'YY'])
                        if id_type == 'HH':
                            qml.Hadamard(wires=wire)
                            qml.Hadamard(wires=wire)
                        elif id_type == 'SSSS':
                            for _ in range(4):
                                qml.S(wires=wire)
                        elif id_type == 'XX':
                            qml.PauliX(wires=wire)
                            qml.PauliX(wires=wire)
                        elif id_type == 'ZZ':
                            qml.PauliZ(wires=wire)
                            qml.PauliZ(wires=wire)
                        elif id_type == 'YY':
                            qml.PauliY(wires=wire)
                            qml.PauliY(wires=wire)
                    qml.apply(op)
                if random.random() < 0.3:
                    wire = random.choice(w_list)
                    qml.Hadamard(wires=wire)
                    qml.Hadamard(wires=wire)
            return new_circuit
            
        func = make_func()
        if isinstance(circuit, qml.QNode):
            qc_list.append(qml.QNode(func, device=circuit.device))
        else:
            qc_list.append(func)
            
    return qc_list
