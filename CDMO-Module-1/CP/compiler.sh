#!bin/bash

for i in {1..5}; do
  for j in {1..7}; do
    in="../CP/instances_dzn/ins-$j.dzn"
    out="../CP/out/out-model$i/out-$j.txt"
    echo;echo;
    echo "time minizinc --solver gecode model$i.mzn $in --output-to-file $out --time-limit 300000"
    time minizinc --solver gecode src/model$i.mzn $in --output-to-file $out --time-limit 300000
  done
done
