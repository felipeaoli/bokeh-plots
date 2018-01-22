from __future__ import division
#
# Scalar_metrics.py version 22-Jan-2018
# To do: Finish the documentation
#    ==> All steps_color 
#    ==> Fixed for the case in which the pipeline breaks 

class LoadMetrics:
    """ Read values from the yaml's files and return an alert (NORMAL, WARN or ALARM)
    associated to a given metric. It also attributes a color for a wedge in the interface 
    CORRECTING WXSIGMA

    Functions:
    ----------     
        Load_qa(qa)
        Load_metrics_n_tests()
        keys_from_scalars(  params_keys)
        test_ranges(qa, kind_of_test)
        qa_status(qa)
        step_color( step_name)
    """
    silent = 'False' # Defining a silent mode
    prfx = 'ql-'
    qa_name    = ['countpix', 'getbias', 'getrms'
                   , 'xwsigma', 'countbins', 'integ'
                   , 'skycont', 'skypeak', 'skyresid', 'snr']
    
    params_keys = [['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO']
               , ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE']
               , ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE']
               , ['B_PEAKS', 'R_PEAKS', 'XSHIFT_ALARM_RANGE', 'WSHIFT_ALARM_RANGE'
                              , 'Z_PEAKS', 'WSHIFT_WARN_RANGE', 'XSHIFT_WARN_RANGE']
               , ['CUTHI', 'CUTLO', 'CUTMED', 'NGOOD_ALARM_RANGE', 'NGOOD_WARN_RANGE']
               , ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE']
               , ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'Z_CONT', 'R_CONT']
               , ['B_PEAKS', 'R_PEAKS', 'SUMCOUNT_WARN_RANGE', 'SUMCOUNT_ALARM_RANGE', 'Z_PEAKS']
               , ['PCHI_RESID', 'PER_RESID', 'SKY_ALARM_RANGE', 'SKY_WARN_RANGE', 'BIN_SZ']
               , ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG']]
    
    params_dict = {'countbins': ['CUTHI', 'CUTLO', 'CUTMED', 'NGOOD_ALARM_RANGE', 'NGOOD_WARN_RANGE'],
                'countpix': ['NPIX_ALARM_RANGE', 'CUTHI', 'NPIX_WARN_RANGE', 'CUTLO'],
                'getbias': ['DIFF_ALARM_RANGE', 'PERCENTILES', 'DIFF_WARN_RANGE'],
                'getrms': ['RMS_ALARM_RANGE', 'RMS_WARN_RANGE'],
                'integ': ['MAGDIFF_ALARM_RANGE', 'MAGDIFF_WARN_RANGE'],
                'skycont': ['SKYCONT_ALARM_RANGE', 'SKYCONT_WARN_RANGE', 'B_CONT', 'Z_CONT', 'R_CONT'],
                'skypeak': ['B_PEAKS', 'R_PEAKS', 'SUMCOUNT_WARN_RANGE'
                             , 'SUMCOUNT_ALARM_RANGE',  'Z_PEAKS'],
                'skyresid': ['PCHI_RESID',  'PER_RESID', 'SKY_ALARM_RANGE', 'SKY_WARN_RANGE', 'BIN_SZ'],
                'snr': ['FIDSNR_WARN_RANGE', 'FIDSNR_ALARM_RANGE', 'FIDMAG'],
                'xwsigma':  ['B_PEAKS',  'R_PEAKS',  'XSHIFT_ALARM_RANGE', 'WSHIFT_ALARM_RANGE'
                             ,  'Z_PEAKS',  'WSHIFT_WARN_RANGE',  'XSHIFT_WARN_RANGE']}
    
 
    

    def __init__(self, cam,exp,night):
        self.cam   = cam
        self.exp   = exp
        self.night = night
        # This is True if the pipeline didn't generate some yaml file
        self.error = dict(zip(self.qa_name, ['False']*len(self.qa_name)) )
        
        print('check *rms_over *bias *SUMCOUNT_RMS shouldbe SUMCOUNT_MED_SKY'
                 +'Resigf  skyresid- residrms')
        # QA tests and keys to respective values
        self.metric_qa_list  = ['getbias','getrms','skycont', 'countbins', 'countpix', 'snr'
                                ,'skyresid', 'skypeak',  'integ',  'xsigma', 'wsigma'   ] #THIS LINE : TB CHECKED
        self.metric_key_list = ['BIAS','RMS_OVER','SKYCONT','NGOODFIBERS', 'NPIX_LOW', 'ELG_FIDMAG_SNR'
                                ,'RESID_RMS', 'SUMCOUNT_MED_SKY', 'MAGDIFF_AVG', 'XSHIFT', 'WSHIFT']
        self.metric_dict     = dict(zip(self.metric_qa_list, self.metric_key_list))

        try: #ff
            self.metrics, self.tests = self.Load_metrics_n_tests()
        except: #ff
            print("Could not load metrics and tests" )
        

        
        
    def Load_qa(self, qa):
        """loads a single yaml file ( rather slow!)
         
        Arguments
        ---------
        qa --
        cam --
        exp --
        night --
        Return
        ------
        y2: list
        """
        import yaml
        cam, exp, night = self.cam, self.exp, self.night
        qlf_folder = '/home/foliveira/'
        exp_folder = 'quicklook/spectro/redux/exposures/'
        aux = '{}{}{}/{}/{}{}-{}-{}.yaml'.format(qlf_folder,exp_folder, night, exp, self.prfx, qa, cam,exp)
        try:
            y2 = yaml.load(open(aux, "r"))
            print ('loading {}'.format(qa))
            self.error.update({qa:False})

        except:
            y2 = None
            print ('{}: yaml not found'.format(qa) )
            #self.error.update({qa:True})
        print ( aux )

        return y2 

    
    def Load_metrics_n_tests(self):
        """ Gathers all the yaml info in 'METRICS' and 'PARAMS'
        and returns them in individual dictionaries
        Uses: Load_qa

        Arguments
        ---------
        qa_name: lst or str
            A name or list of names of qa's

        Return
        ------
        dic_met: dictionary
            A dictionary with the metric values 
        
        dic_test: dictionary
            A dictionary with the test values
    
        """
        dic_met = {}
        dic_tst = {}
        
        if isinstance(self.qa_name, list):
            qa_list = self.qa_name
        elif isinstance(self.qa_name, string): # for a single qa_name
            qa_list = [self.qa_name]
        else:
            return "Invalid QA format"
            
        for i in qa_list:
            aux = self.Load_qa(i)
            if aux == None:
                dic_met.update({i: aux})
                dic_tst.update({i: aux})
                self.error.update({i:True})
            else:
                dic_met.update({i: aux['METRICS']})
                dic_tst.update({i: aux['PARAMS']})
        return dic_met, dic_tst


    def keys_from_scalars(self,  params_keys):    
        """ Finds the equivalente alert keys in yaml for a metric.

        Arguments
        ---------
        qa_name: list
            A list of str w/ the QA names
        params_keys: list
            List of list of str w/ keys names contained in METRICS.    

        Return
        -------
        xx: dict
            A  dictionary of <qa_name>. For each 'qa_name' another dictionary with  {kind_of_test>,
            addressing a 'kind of test' to its equivalent key inside the yaml file.
        """       
        xx = {}
        #qa_name, params_keys = self.qa_name, self.params_keys
        params_keys =  self.params_keys

        for index, scalar in enumerate(self.qa_name):
            if scalar=='xwsigma': # Redistrubuting xsigma and wsigma
                xx['xsigma'] = {'alarm':'XSHIFT_ALARM_RANGE', 'warn':'XSHIFT_WARN_RANGE'}
                xx['wsigma'] = {'alarm':'WSHIFT_ALARM_RANGE', 'warn':'WSHIFT_WARN_RANGE'}
                xx.update({'xsigma':{'alarm':'XSHIFT_ALARM_RANGE', 'warn':'XSHIFT_WARN_RANGE'}
                          ,'wsigma':{'alarm':'WSHIFT_ALARM_RANGE', 'warn':'WSHIFT_WARN_RANGE'}})
            else:
                for j in params_keys[index]:
                    #print j
                    if 'ALARM_RANGE' in j:
                        alarm_name =  j
                    
                    if 'WARN_RANGE' in j:
                        warn_name  = j
                try:
                    xx.update({scalar: {'alarm':alarm_name, 'warn':warn_name}})
                except:
                    print ('Error during dictionary update')
        return xx   
    
    
    def test_ranges(self, qa, kind_of_test):
        """ Returns the range of a given test from the yaml file.

        Arguments
        ---------
        qa: ?list
            ?d
        kind_of_test: ?list
            ?d

        Return
        ------
        test_range: list
            A list representing [min_value, max_value]
        """      
        self.qa = qa
        self.kot = kind_of_test
        qa_name  = ['countpix', 'getbias', 'getrms'
                   , 'xwsigma', 'countbins', 'integ'
                   , 'skycont', 'skypeak', 'skyresid', 'snr']
        
        metrics = self.metrics
        tests   = self.tests 

        self.par_k   = self.params_keys
        #self.d  = self.keys_from_scalars(qa_name, self.par_k)#f
        self.d  = self.keys_from_scalars(self.par_k)
        qalist  = qa_name + ['xsigma', 'wsigma']
    
        if self.kot not in ['warn', 'alarm']:
            raise Exception('Error: Invalid test value:', self.kot)
        
        if   self.qa == 'xwsigma':
            raise Exception('Error: Please use either xsigma or wsigma.')  
        elif self.qa not in qalist: 
            raise Exception('Error: Invalid QA name:', qa)
        elif(self.qa in ['xsigma', 'wsigma']):
            qa_2       = 'xwsigma'        
            test_range = tests[qa_2][self.d[self.qa][self.kot]]
        else:
            test_range = tests[qa][self.d[self.qa][self.kot]]
        
        return test_range

       

    def qa_status(self, qa):
        """Returns the alert of a given qa

        Arguments
        ---------
        qa: str
       
        Return
        ------
        status: str
            Possible values: 'NORMAL', 'WARN' or 'ALARM'
        """
        #self.qa = qa  
        if qa == 'xwsigma':
            alarm_x = self.test_ranges('xsigma','alarm')
            warn_x = self.test_ranges('xsigma','warn')
            val_x = self.metrics[qa][self.metric_dict['xsigma']]

            alarm_w = self.test_ranges('wsigma','alarm')
            warn_w = self.test_ranges('wsigma','warn')
            val_w = self.metrics[qa][self.metric_dict['wsigma']]

            if isinstance(val_w,float) or isinstance(val_w, int) or isinstance(val_x,float) or isinstance(val_x, int):
                pass
            else:
                raise Exception ("Invalid variable type in xwsigma: {} or {}".format(val_x, val_w))
        
            if( val_w <= alarm_w[0] or val_w >= alarm_w[1] or val_x <= alarm_x[0] or val_x >= alarm_x[1]): 
            # ">=" comes from pipeline definition!
                return 'ALARM'
            elif(val_x <= warn_x[0] or val_x >= warn_x[1] or val_w <= warn_w[0] or val_w >= warn_w[1] ):
                return 'WARN' 
            else:
                return 'NORMAL' 

        elif(qa == 'xsigma' or qa == 'wsigma'):
            print('Please, use xwsigma')
            return 'Error'

        # Original
        else:               
            alarm = self.test_ranges(qa,'alarm')
            warn  = self.test_ranges(qa,'warn')
            val   = self.metrics[qa][self.metric_dict[qa]]
        #dbprint(qa, self.metric_dict[qa])

        if val ==[]:
            return 'ALARM'

        if isinstance(val,float) or isinstance(val, int):
            pass
        else:
            self.error.update({qa:True})
            raise Exception ("Invalid variable type:{} in".format(val), qa)

        
        if ( val <= alarm[0] or val >= alarm[1]): # ">=" comes from pipeline definition!
            return 'ALARM'
        elif (val <= warn[0] or val >= warn[1] ):
            return 'WARN' 
        else:
            return 'NORMAL'


       
    def step_color(self, step_name):
        """ Colors for the wedges in a given step of the pipeline
        FOR WHILE PARTIAL!!!: Until we find all scalars
        Missing: Xsigma and Wsigma
        Arguments
        ---------
        step_name: str
            The abbreviated name of one of the four QA steps
        Return
        ------
        color: str
            Wedge color Alert
        """
        self.step_name = step_name
        steps_list = ['preproc', 'extract', 'fiberfl', 'skysubs']
        if not isinstance(self.step_name, str): 
            return "{} is not a String".format(self.step_name)
        if self.step_name not in steps_list:
            return "Invalid step: please return a value in {}".format(steps_list)
    
        steps_dic = {'preproc':['countpix', 'getbias','getrms', 'xwsigma'],
                     'extract':['countbins'],
                     'fiberfl':['integ','skycont','skypeak','skyresid'],
                     'skysubs':['snr']}
        steps_status = []

        print ( 'init_error', self.error    )
        for i in steps_dic[self.step_name]:
            print (i, self.error[i])
            if(self.error[i]):
                print ('QL FAILURE')
                steps_status.append('FAILURE')
                
            else:
                aux1 = self.qa_status(i)
                steps_status.append(aux1)
                #pass
       
        #for i in PARTIALsteps_dic[self.step_name]:
        #    steps_status.append(self.qa_status(i))
        print( 'Steps_status:', steps_status)

        if any(x=='FAILURE' for x in steps_status):
            color = 'magenta' # Pick a color for failure case
        
        elif any( x == 'ALARM'  for x in steps_status):
            color =  "red"
            print( color )
        elif any( x == 'WARN'  for x in steps_status):
            color =  "yellow"
            print( color )
        elif all(x=='NORMAL' for x in steps_status): #intentionally redundant
            color = "green"
            print( color )
        return color


        
# *************************************************************************        
if __name__=="__main__":
    #test 03 colors for wedges:

    cam, exp, night = 'z0', '00000003', '20190101'

    lm = LoadMetrics(cam, exp, night)

    print(lm.step_color('preproc'))

    """    
    cam, exp, night = 'z0', '00000003', '20190101'
    print ("\n\nTests for the available scalars and using yaml output\n"\
            , "="*50)
    print ("TO DO:\n *docs of functions \n *what more else?")
   
    # test 01
    lm = LoadMetrics(cam, exp, night)
    print(lm.PARTIALstep_color('preproc'))
    """
    """
    print lm.keys_from_scalars('getbias','warn')
    print lm.test_ranges('getbias', 'warn')
    print lm.qa_status('countpix')
    
    
    # test 02: 
    print '\nEvaluated here:\n' 
    my_metrics = lm.metrics
    for i in lm.metric_qa_list:
        print '{}: \t{}'.format(i, lm.qa_status(i) )
    
    print '\n\nFrom QL file:'
    #Reading form yaml files
    for j in list(my_metrics):
        for jj in list(my_metrics[j]):
            if '_ERR' in jj:
                print 'In %s \t'%(j),
            print '{}:\t {}'.format(jj, my_metrics[j][jj])
    steps_dic = {'preproc':['countpix', 'getbias','getrms','wsigma', 'xsigma'],
              'extract':['countbins'],
              'fiberfl':['integ', 'skycont', 'skypeak', 'skyresid'],
              'skysubs':['snr']}
    print lm.metric_qa_list

    #test 03 colors for wedges:
    cam, exp, night = 'z7', '00000003', '20190101'
    lm = LoadMetrics(cam, exp, night)
    lm.PARTIALstep_color('sn')
    """
