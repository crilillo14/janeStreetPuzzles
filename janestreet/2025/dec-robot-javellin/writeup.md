Q: Java-lin v. Spears Robot

Two robots play a javellin throwing game.  
Both their first throws are \(T_1 \sim U(0, 1)\).  
Their first throws are private information.  
They can choose to throw a second javellin, with the same distance distribution, but they would have to stay with it.

Guess: Nash Equilibrium is some set of strategies in a symmetric game:

> Robot X: Throw again if \(T_{1} < \mathbb{E}[T_2] = 0.5\), else keep the first throw.

But then, SR gains an edge, getting a single bit of info on if the first throw of Java-lin is \(>\) or \(<\) some \(d \in [0 , 1]\).

Then, the game deviates from the NE and a separate strategy is formed for SR: 

> Javalin {  
> &nbsp;&nbsp;don't throw \(T_{2,J}\) if \(T_{1,J} > 0.5\)  
> &nbsp;&nbsp;else throw  
> }

Spears Robot {  
&nbsp;&nbsp;throw again if  
\[
\mathbb{E}[T_{2,S} \mid T_{1,S},\, T_{1,J} > d] = 0.5
\]  
&nbsp;&nbsp;else throw  
}

