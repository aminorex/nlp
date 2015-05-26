#!/usr/bin/env lua
require ("pecco")

table.insert (arg, 1, "$0")
timer = pecco.Timer ("pecco", "classify")
opt   = pecco.option (#arg, arg)
c     = pecco.kernel_model (opt)
c:load (opt.model)

pp, pn, np, nn = 0, 0, 0, 0
for line in io.lines (opt.test) do
   local label = string.match (line, "^%S+")
   local fstr = string.sub (line, string.len (label) + 1)
   timer:startTimer ()
   local fv = {}
   for f in string.gmatch (fstr, " (%d+)") do
     fv[#fv+1] = tonumber (f)
   end
   sign = c:binClassify (fv)
   timer:stopTimer ()
   if label == "+1" then
      if sign then pp = pp + 1 else pn = pn + 1 end
   else
      if sign then np = np + 1 else nn = nn + 1 end
   end
end

io.stderr:write (string.format ("acc. %.4f (pp %d) (pn %d) (np %d) (nn %d)\n",
                                (pp + nn) * 1.0 / (pp + pn + np + nn), pp, pn, np, nn))

timer:printElapsed ();
