#!/usr/bin/env python
# Usage: to_pecco.py model
#  check whether pecco can handle model and reformat if needed
import sys, re

if len (sys.argv) < 2:
    sys.exit ("Usage: %s model" % sys.argv[0])

model  = sys.argv[1]
lines  = open (model).readlines ()
signature = lines[0][:-1].split (' ')

learner = 'MaxEnt'
sys.stderr.write ("checking %s..\n" % model)
if signature[0] == 'svm_type': # LIBSVM
    if signature[1][-3:] == 'svc':
        learner = 'LIBSVM'
        _, kernel  = lines[1][:-1].split (' ')
        if kernel != 'linear' and kernel != 'polynomial':
            sys.exit ("unsupported kernel type: %s\n" % kernel)
    else:
        sys.exit ("only c_svc and nu_svc supported\n")
        kernel = kernel != 'linear' and 1 or 0
elif len (signature) != 1: # not MaxEnt
    learner = signature[0]
    if learner != 'opal':
        kernel  = int (lines[1].split (' ')[0])
        if kernel != 0 and kernel != 1:
            sys.exit ("unsupported kernel type: %s\n" % kernel)

sys.stderr.write ("    learner: %s\n" % learner)

if re.match (r'^(opal|MaxEnt|TinySVM)$', learner): # natively supported
    if learner == 'opal':
        pass # natively supported
    elif learner == 'TinySVM':
        # examine the validity of feature value in support vectors
        body = False
        for line in lines[1:]:
            if body: # assert feature value = 1
                if not reduce (lambda x, y: x & y,
                               [float (x.split (':')[1]) == 1.0
                                for x in line[:-1].split (' ')[1:]]):
                    sys.exit ("only binary features are supported:\n  %s" % line)
            else:
                body |= line.find ('# threshold b') != -1
    elif learner == 'MaxEnt':
        # examine the validity of feature format
        poly_d = 0
        for line in lines:
            if line.count ('\t') != 2:
                sys.exit ("MaxEnt: irregular feature format\n")
            label, feature, weight = line[:-1].split ('\t')
            if re.match (r'\d+(?::\d+){0,3}$', feature):
                features = feature.split (':')
                if len (features) != len (set (features)):
                    sys.exit ("MaxEnt: duplicated feature id: %s\n" % lfw[1])
                poly_d = max (poly_d, len (features))
            else:
                sys.exit ("feature '%s' is not in supported format: '\d+(?::\d+){0,3}\n" % feature)
        sys.stderr.write ("    degree:  %d\n" % poly_d)
    sys.stderr.write ("\nnatively supported; input %s to pecco.\n" % model)
else:
    # linear kernel = polynomial kernel of (1 w * x + 0)^1
    f = open ('pecco_' + model, "w")
    f.write ("%s; converted by pecco:tools/to_pecco.py\n" % lines[0][:-1])
    #
    body = False
    if learner == 'LIBSVM':
        rev  = False # if label '+1' is set to negative, swap positive/negative
        bias = '0'
        for line in lines[1:]:
            if body: # assert feature value = 1
                fv = line.rstrip ().split (' ')
                alpha = fv.pop (0)
                if not reduce (lambda x, y: x & y,
                               (float (x.split (':')[1]) == 1.0 for x in fv)):
                    sys.exit ("only binary features are supported:\n  %s" % line)
                if rev:
                    alpha = alpha[0] == '-'  and alpha[1:] or '-' + alpha
                f.write ("%s %s\n" % (alpha, ' '.join (fv)))
            elif line[:-1] == 'SV':
                body = True
            else:
                param, value = line[:-1].split (' ')[:2]
                if param == 'rho':
                    bias = value
                elif param == 'nr_class':
                    if int (value) != 2:
                        sys.exit ("\nsorry, multi-class model is not supported.")
                elif param == 'label':
                    if int (value) != 1: # 1 as negative -> positive
                        rev = True
                        bias = bias[0] == '-' and bias[1:] or '-' + bias
                    f.write ('%s # threshold b\n' % bias)
                elif param == 'kernel_type':
                    f.write ('%s # kernel type\n' % (value != 'linear' and 1 or 0))
                elif param == 'degree':
                    f.write ('%s # kernel parameter -d\n' % value)
                elif param == 'gamma':
                    f.write ('%s # kernel parameter -s\n' % value)
                elif param == 'coef0':
                    f.write ('%s # kernel parameter -r\n' % value)
    else: # svm-light
        for line in lines[1:]:
            if body: # assert feature value = 1
                fv = line.split ('#')[0].rstrip ().split (' ') # clip comments
                alpha = fv.pop (0)
                if not reduce (lambda x, y: x & y,
                               [float (x.split (':')[1]) == 1.0 for x in fv]):
                    sys.exit ("only binary features are supported:\n  %s" % line)
                f.write ("%s %s\n" % (alpha, ' '.join (fv)))
            else:
                f.write ("%s\n" % line.rstrip ()) # clip trailing spaces
                body |= line.find ('# threshold b') != -1
    f.close ()
    sys.stderr.write ("\nsupported; input %s to pecco.\n" % f.name)
