### 📖 Chapter I

#### The octopus orchestra

Moore's Law: New process appear 2 years after the predecessors

##### Latency vs Throughput
Latency is how much time a task is needed to complete
Throughput is how much work can be done in X

**Analogy: The Coffee Shop**

Imagine a coffee shop.

*   **Latency** is the total time it takes for you to get your coffee, from the moment you place your order to the moment you have it in your hand. Let's say this takes 5 minutes.

*   **Throughput** is the total number of coffees the shop can produce in a given period, say, an hour. If the shop can serve 12 customers in an hour, its throughput is 12 coffees/hour.

Now, if the coffee shop adds another barista and another coffee machine (an example of concurrency), the **latency** for a single coffee might not change—it still takes 5 minutes to make one coffee. However, since they can now serve two customers at once, the **throughput** doubles to 24 coffees/hour.

In this analogy:
- **Reducing latency** would mean making a single coffee faster (e.g., a more efficient coffee machine).
- **Increasing throughput** means serving more customers in the same amount of time (e.g., adding more baristas and machines).

Concurrency can reduce latency.
It can hide latency.
It can increase throughput = make the system able to do more work.

#### Solving complex and large problems

Complexity can come from the size of the problem or how hard is to understand a given piece of the system we develop
Scalability: characteristic of the system that can improve perfomance just adding more resources.

####  Layers of concurrency

- Conceptual layers: the code or the music
- Runtime layers: the musicans
- Low level layer: hardware the specific instrument

