#! /usr/bin/env bbpy
import os
import sys
import copy
import random
import json
import bas
from bdet import Date
from bdet import Time
from bdet import Datetime
from bdet import DatetimeTz


# Provides interface for Tadatasv
class Tadatasv:
    def __init__(self, uuid=2289087, firm=9001, timeout=60):
        self.uuid = uuid
        self.user_ident = bas.UserIdent.factory(uuid=uuid, firmNumber=firm)
        self.workstation_no = 0
        self.serial_no = 0
        self.timeout = timeout   
        descriptor = bas.lookup('tadatasv', 1, 20)
        self.svcHandle = descriptor.tcpClient(
            userIdent=self.user_ident, timeout=self.timeout)

    def make_request(self,requestId,start,end,periodicity,fields=None):

        if not fields:
            if periodicity >= 86400:
                fields = [ "PR006", "PR007" , "PR008" , "PR005", "PR013", "PR093" ]
            else:
                fields = [ "PR006", "PR007" , "PR008" , "PR005", "PR013", "PR093", "TICK_COUNT" ]

        rangeInfo = {
                'startDateTimeInfo' : {
                    'dateTimeTz' : start
                    },
                'endDateTimeInfo' : {
                    'dateTimeTz' : end
                    },
                'periodicity' : periodicity,
                'sessionInfo' : {},
                'sessionTimeStampInfo' : "TIME_STAMP_START_END_DATE_TIME_GMT_EPOCH",
                'dataTimeStampInfo' : 'TIME_STAMP_GMT_EPOCH_TIME',
                'prepend' : 0,
                'retrieveTradeDates' : True
                }
            
        objInfo = {
                'securityName' : parsekey,
                'timeSeriesFieldsList' : {
                    'list' : fields,
                    'dataValuesFormat' : 'DATA_VALUE_DOUBLES',
                    },
                'dataRequestDateTimeInformation' : rangeInfo,
                'fetchSessions' : True,
                'overrides' : {},
                'subRequestId' : int(random.random()*10000),
                }

        request = {
                'requestId' : requestId,
                'userInfo' : {
                    'uuid' : self.uuid,
                    'serialNum' : self.serial_no,
                    'workstationNum' : self.workstation_no,
                    'serialNumMode' : "SN_OMITTED_USER_IS_BBA"
                    },
                'securityInfoList' : {
                    'list' : [ objInfo ]
                    },
                'attributeList' : {
                    'attributes' : None
                    },
                'usePartialResponse' : False,
                }

        return request

    def make_singular(self,requestId,parsekey,fields):
        return {
            'requestId' : requestId,
            'userInfo' : {
                'uuid' : self.uuid,
                'serialNum' : self.serial_no,
                'workstationNum' : self.workstation_no,
                'serialNumMode' : "SN_OMITTED_USER_IS_BBA"
                },
            'securityInfoList' : {
                'list' : [ { 
                        'securityName' : parsekey,
                        'singularFieldsList' : {
                            'list' : fields,
                            'dataValuesFormat' : 'DATA_VALUE_DOUBLES'
                            }
                        } ]
                }
            }

def write_response(r,f,i,verbosity=0,headeronly=False):
    rows = [ [],[],[],[],[],[],[], [] ]
    fields= ['gmtEpochTime']
    npoints = 0

    try:
        nitems = 0
        nrows = 0
        col_num = 0
        tsdr = r['timeSeriesDataResponse']
        rd = tsdr['resultData']
        rdi = rd['resultDataItems']
        for info in rdi:
            nitems += 1
            rtsdi = info['resultTimeSeriesDataInfo']
            if not 'resultTimeSeriesDataDoubles' in rtsdi:
                continue
            rtsdd = rtsdi['resultTimeSeriesDataDoubles']
            ts = rtsdd['timeStamp']
            times = ts['gmtEpochTime']
            col_num = 0
            for time in times:
                rows[col_num].append(int(time))
            nrows = len(rows[col_num])
            
            items = rtsdd['timeSeriesDataItems']
            for item in items:
                col_num = len(fields)
                if col_num >= len(rows):
                    raise Exception('Excess columns '+repr(col_num)+' '+repr(len(rows))+' '+item['fieldName'])
                fields.append(item['fieldName'])
                fvs = item['fieldValues']
                for val in fvs['values']:
                    rows[col_num].append(float(val))
                if verbosity > 0:
                    print nitems,col_num,nrows,len(rows[col_num])

        if col_num != len(fields):
            raise Exception('Mismatch columns '+repr(col_num)+' '+repr(len(fields)))
        if (nrows and not i) or (headeronly and col_num > 1):
            for ii in range(0,len(fields)):
                f.write((',"' if ii else '"')+fields[ii]+'"')
            f.write("\n")
            if headeronly:
                return -1
        if headeronly:
            return 0

        for row in range(0,nrows):
            for col in range(0,col_num+1):
                f.write(('' if col == 0 else ',')+repr(rows[col][row]))
                npoints += 1
            f.write("\n")

        if verbosity > 0:
            print npoints

    except:
        o,t,m = sys.exc_info()
        sys.excepthook(o,t,m)
        return -2

    return npoints


def month_length(m,y):
    if m > 7:
        return 31 - (y % 2)
    elif m == 2:
        return 28 if  y % 4 else 29
    else:
        return 30 + (y % 2)

def fetch_series(svc,parsekey,outf,periodicity=3600,verbosity=0,headeronly=False):
    iter = 0
    if verbosity > 0:
        print parsekey

    for year in range(2009,2015):
        for month in range(1,13):
            if periodicity < 14400:
                mlen = month_length(month,year)
                for day in range(0,mlen):
                    requestId = int(random.random()*10000)
                    start = Datetime(Date(year,month,day+1),Time(0,0,0))
                    if day == mlen - 1:
                        day = -1
                        if month == 12:
                            year += 1
                            month = 1
                        else:
                            month += 1
                    end = Datetime(Date(year,month,day+2),Time(0,0,0))
                    request = svc.make_request(requestId,start,end,periodicity)
                    response = svc.svcHandle.timeSeriesDataRequest(request)._toPy()

                    npoints = write_response(response,outf,iter,verbosity-1,headeronly=headeronly)
                    if headeronly:
                        if npoints == -1:
                            return True
                    elif npoints < 1:
                        print 'failed:',iter,requestId,parsekey,year,month,day+2
                        print 'request:',repr(request)
                        print 'response:',repr(response)
                    elif verbosity > 0:
                        print iter,requestId,year,month,day+2
                    iter += 1
            else:
                requestId = int(random.random()*10000)
                start = Datetime(Date(year,month,1),Time(0,0,0))
                end = Datetime(Date(year+(1 if month == 12 else 0),
                                    month+1 if month < 12 else 1,
                                    1),
                               Time(0,0,0))
                request = svc.make_request(requestId,start,end,periodicity)
                response = svc.svcHandle.timeSeriesDataRequest(request)._toPy()
                
                npoints = write_response(response,outf,iter,verbosity-1,headeronly=headeronly)
                if headeronly:
                    if npoints == -1:
                        return True
                elif npoints < 1:
                    print 'failed:',iter,requestId,parsekey,year,month
                    print 'request:',repr(request)
                    print 'response:',repr(response)
                elif verbosity > 0:
                    print iter,requestId,year,month
                iter += 1
    return False

# Use the main to test the the class
if __name__ == "__main__":

    if 'blp' in os.listdir('data'):
        os.chdir('data/blp')

    verbosity = 0
    headeronly = False
    periodicity = 3600
    calcrt = False
    fields = []
    args = ""
    for arg in sys.argv[1:]:
        if arg == '-v':
            verbosity += 1
        elif arg == '-c':
            calcrt = True
        elif arg == '-H':
            headeronly=True
        elif calcrt and all(map(lambda x: len(x) == 5,arg.split(','))):
            for x in arg.split(','):
                fields.append(x)
        elif arg[0].isdigit():
            periodicity = int(arg)
        else:
            args +=" "+arg

    random.seed(os.urandom(4))

    args = args.strip()
    parsekeys = []
    file_p = False
    if os.access(args,os.R_OK):
        file_p = True
        for line in open(args,'r'):
            if line[0] == '#':
                continue
            csvs = line.split(',')
            if len(csvs) > 1:
                parsekeys.append(csvs[1])
    elif args:
        parsekeys.append(args)
    else:
        print 'No securities specified'
        sys.exit(1)

    if verbosity:
        print len(parsekeys),'securities to pull...'

    svc = Tadatasv()

    if calcrt:
        data = None
        try:
            for parsekey in parsekeys:
                id = int(random.random()*10000)
                data = svc.svcHandle.singularDataRequest(svc.make_singular(id,parsekey,fields))._toPy()
                data = data['singularDataResponse']
                data = data['singularResultData']
                data = data['singularResultDataItems']
                for item in data:
                    for field in item['resultFields']:
                        name = field['fieldName']
                        vtyp = field['fieldValueType']
                        fval = field['fieldValue']
                        print parsekey,vtyp,name,'=','"'+fval+'"'
        except:
            o,t,m = sys.exc_info()
            sys.excepthook(o,t,m)
            print repr(data)
            sys.exit(1)
        sys.exit(0)

    nokay = 0
    nfail = 0
    nskip = 0
    for parsekey in parsekeys:
        path = parsekey.replace(' ','_')+(".hdr" if headeronly else ".csv")
        if not file_p or not os.access(path,os.R_OK):
            outf = open(path,'w')
            okay = fetch_series(svc,parsekey,outf,periodicity,verbosity,headeronly)
            outf.close()
            if okay:
                nokay += 1
                if verbosity:
                    print path,'okay'
            else:
                nfail += 1
                if verbosity:
                    print path,'fail'
        else:
            if verbosity:
                print path,'skip'
            nskip += 1

    print nokay,'fetched'
    print nfail,'failed'
    print nskip,'skipped'
    sys.exit(0)
