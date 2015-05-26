#!/usr/bin/env ruby
require 'pecco'

ARGV.unshift("$0")
timer = Pecco::Timer.new("pecco", "classify")
opt   = Pecco::Option.new(ARGV.length, ARGV)
c     = Pecco::Kernel_model.new(opt)
c.load(opt.model);

f     = open(opt.test)
pp, pn, np, nn = 0, 0, 0, 0
while line = f.gets do
  line.chomp =~ /^(\S+) /
  label, fstr = $1, $'
  timer.startTimer()
  fv = fstr.split(' ').map {|x| x.split(':')[0].to_i}
  sign = c.binClassify(fv)
  timer.stopTimer()
  if label == "+1" then
    if sign then pp += 1 else pn += 1 end
  else
    if sign then np += 1 else nn += 1 end
  end
end
f.close

STDERR.printf("acc. %.4f (pp %d) (pn %d) (np %d) (nn %d)\n",
              (pp + nn) * 1.0 / (pp + pn + np + nn), pp, pn, np, nn)

timer.printElapsed()
