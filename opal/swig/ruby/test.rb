#!/usr/bin/env ruby
require 'opal'

opt = Opal::Option.new(ARGV.size + 1, ["$0"] + ARGV);

timer = Opal::Timer.new("train")
m = Opal::Model.new(opt)

timer.startTimer()
m.train_from_file(opt.train, opt.iter, opt.output == 1 ? opt.test : "")
m.save(opt.model)
timer.stopTimer()

timer.printElapsed();

timer = Opal::Timer.new("test")
m = Opal::Model.new(opt)
m.load(opt.model)

timer.startTimer()
# m.test_on_file(opt.test, opt.output)
corr = incorr = 0
f = open(opt.test)
while line = f.gets do
  y, *x = line.split(" ")
  x = x.map {|x| x.split(":")[0].to_i }
  y_ = m.binClassify(x) ? '+1' : '-1'
#  y_ = m.getLabel(x) # for multiclass
  if y == y_ then corr += 1 else incorr += 1 end
end
printf("acc. %.4f\n", corr.to_f / (corr + incorr))
f.close

timer.stopTimer()

timer.printElapsed();
