hatch run simple --model_type='hit' --solver_name='GUROBI'
hatch run simple --model_type='payment' --solver_name='GUROBI'
hatch run simple --model_type='combined' --solver_name='GUROBI'
hatch run relaxed --solver_name='GUROBI' --model_type='hit' --slacks="0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.995, 0.999"
hatch run combination --solver_name='GUROBI' --base_model_type='hit'
hatch run relaxed --solver_name='GUROBI' --model_type='payment' --slacks="0.95, 0.96, 0.97, 0.98, 0.985, 0.99, 0.995, 0.999"
hatch run combination --solver_name='GUROBI' --base_model_type='combined'
hatch run combination --solver_name='GUROBI' --base_model_type='payment'
