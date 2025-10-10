### 📖 Chapter II


#### Serial and parallel execution

Serial execution: Following a order and not advance until the precedding step is completed.
One after another is the serially mode.

Concurrency: is based on the idea that are independent computations that can be executed in any order.


Parallelal execution: Increasing the throughput in the same time. Task independence: means processomg resources can process tasks in
whatever order they like and wherever they like, as long as the result is the same.
Embarrasignly parraelal usually refers to an algorithim with low communications needs.

Amdahl's law: The counterintuitive thought that adding more resources can executer tasks faster.
Gustafon's law: If we keep increasing the amount of work, the sequentias pars will have less and less effect.

#### Concurrency vs parallelism

- An application can be concurrent but no parallel. It processes more than one task over a given period
- An application can be parallela but not concurrent, which means it proccesses multiple subtaks of a single task simulatenously.
- An application can be both parallel and concurrent, which emans it processes multiple tasks or
subtkas of a single task concurrently at the same time

