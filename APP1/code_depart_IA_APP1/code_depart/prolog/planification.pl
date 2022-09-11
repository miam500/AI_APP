move(Env, X) :- member(coin(X), Env); member(treasure(X), Env); member(block(X), Env); member(empty(X), Env); member(monster(X), Env); member(goal(X), Env).
actionsPossibles(Env, Res) :- findall(Action, move(Env, Action), Res).

