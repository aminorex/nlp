#!/usr/bin/env lua
require ("opal")

table.insert (arg, 1, "$0")
opt   = opal.option (#arg, arg)

timer = opal.Timer ("train")
m = opal.Model (opt)

timer:startTimer ()
if opt.output == 1 then
   m:train_from_file (opt.train, opt.iter, opt.test)
else
   m:train_from_file (opt.train, opt.iter)
end
m:save (opt.model)
timer:stopTimer ()

timer:printElapsed ();

timer = opal.Timer ("test")
m = opal.Model (opt)
m:load (opt.model)

timer:startTimer ()
-- m:test_on_file (opt.test, opt.output)
corr, incorr = 0, 0
for line in io.lines (opt.test) do
   local y = string.match (line, "^%S+")
   local x = {}
   for f in string.gmatch (line, " (%d+)") do -- no built-in split
      x[#x+1] = f
   end
   local y_ = m:binClassify (x) and "+1" or "-1"
--   local y_ = m:getLabel (x)
   if y == y_ then corr = corr + 1 else incorr = incorr + 1 end
end
print (string.format ("acc. %.4f", corr / (corr + incorr)))

timer:stopTimer ()

timer:printElapsed ();
