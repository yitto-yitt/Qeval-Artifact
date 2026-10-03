# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml
import random

def equivalent_clifford_circuit(circuit, n):
    is_qnode = isinstance(circuit, qml.QNode)
    is_tape = isinstance(circuit, (qml.tape.QuantumTape, qml.tape.QuantumScript))
    
    if is_qnode:
        func = circuit.func
        device = circuit.device
        wires = list(device.wires)
        if not wires:
            try:
                tape = qml.workflow.construct_tape(func)()
                wires = list(tape.wires)
            except:
                wires = [0]
    elif is_tape:
        wires = list(circuit.wires)
        if not wires:
            wires = [0]
    else:
        func = circuit
        try:
            tape = qml.workflow.construct_tape(func)()
            wires = list(tape.wires)
        except:
            wires = [0]
            
    qc_list = []
    for i in range(n):
        if is_tape:
            extra_ops = []
            state = random.Random(i)
            num_identities = state.randint(1, 5)
            for _ in range(num_identities):
                op_type = state.choice(['H', 'S', 'X'])
                wire = state.choice(wires)
                if op_type == 'H':
                    extra_ops.extend([qml.Hadamard(wires=wire), qml.Hadamard(wires=wire)])
                elif op_type == 'S':
                    extra_ops.extend([qml.S(wires=wire), qml.S(wires=wire), qml.S(wires=wire), qml.S(wires=wire)])
                elif op_type == 'X':
                    extra_ops.extend([qml.PauliX(wires=wire), qml.PauliX(wires=wire)])
            new_ops = list(circuit.operations) + extra_ops
            new_tape = qml.tape.QuantumScript(new_ops, circuit.measurements)
            qc_list.append(new_tape)
        else:
            def make_func(f, w, seed):
                def _wrapper(*args, **kwargs):
                    f(*args, **kwargs)
                    state = random.Random(seed)
                    num_identities = state.randint(1, 5)
                    for _ in range(num_identities):
                        op_type = state.choice(['H', 'S', 'X'])
                        wire = state.choice(w)
                        if op_type == 'H':
                            qml.Hadamard(wires=wire)
                            qml.Hadamard(wires=wire)
                        elif op_type == 'S':
                            qml.S(wires=wire)
                            qml.S(wires=wire)
                            qml.S(wires=wire)
                            qml.S(wires=wire)
                        elif op_type == 'X':
                            qml.PauliX(wires=wire)
                            qml.PauliX(wires=wire)
                return _wrapper
            
            new_func = make_func(func, wires, i)
            if is_qnode:
                new_qnode = qml.QNode(new_func, device, interface=circuit.interface)
                qc_list.append(new_qnode)
            else:
                qc_list.append(new_func)
                
    return qc_list
