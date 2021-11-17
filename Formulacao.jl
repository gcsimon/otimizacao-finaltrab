using Cbc
using JuMP

m = Model();

set_optimizer(m, Cbc.Optimizer)

f = open("D:/Trabalhos/Otimização/Problema1/induced_700_73395.dat", "r");

file = read(f, String); 

rawList = split(file, "\n")
rawList = convert(Vector{String}, rawList)
inputFile = []
for (index, value) in enumerate(rawList)
           append!(inputFile,  [convert(Vector{String},split(value, " "))])
       end
pop!(inputFile);


@variable(m, NV >=0)
NumberVertices=parse(Int64,inputFile[1][1])
popfirst!(inputFile)
NV = collect(1:NumberVertices);

@variable(m, G[x in NV, y in NV])
@variable(m, M[x in NV, y in NV], Bin)
@variable(m, X[x in NV] >=0, Int)
@variable(m, Vec[x in NV], Bin);


G = zeros(Int64, NumberVertices, NumberVertices)
for (index, value) in enumerate(inputFile)
    x = parse(Int64, value[1])
    y = parse(Int64, value[2])
    G[x,y] = 1
    G[y,x] = 1
       end
;

@objective(m, Max, sum(Vec[i] for i in NV));

@constraint(m, [i in NV, j in NV], M[i,j] >= (Vec[i] + Vec[j]) * G[i,j] - 1) # Isso é equivalente à 
@constraint(m, [i in NV, j in NV], M[i,j] <= (Vec[i] + Vec[j]) * G[i,j] / 2) # Vec[i] and Vec[j] * G[i,j]
@constraint(m, [i in NV], sum(M[i,j] for j in NV) == 2*X[i]);

set_time_limit_sec(m, 3600.0);

optimize!(m)


