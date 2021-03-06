from __future__ import division
# Scalar_metrics.py version 05-Dec-2017
# To do: Finish the documentation
#        python3 and matplotlib2 (cm.jet)
#    ==> PARTIALsteps_color: It only will be complete when we find all the ALERT criteria!
#    ==> Fixed for the case in which the pipeline breaks 

class LoadMetrics:
    """ Read values from the yaml's files and return an alert (NORMAL, WARN or ALARM)
    associated to a given metric.

    Functions:     Load_qa( qa, cam, exp, night)     Load_metrics_n_tests(self)
    ----------     keys_from_scalars(self,  params_keys)         test_ranges(self, qa, kind_of_test)
                   qa_status(self, qa)                  PARTIALstep_color(self, step_name)
    """
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
    
    # This is True if the pipeline didn't generate some yaml file
    error = dict(zip(qa_name, ['False']*len(qa_name))) 
    

    def __init__(self, cam,exp,night):
        self.cam   = cam
        self.exp   = exp
        self.night = night
        
        # QA tests available for while PARTIAL
        self.metric_qa_list  = ['getbias','getrms','skycont', 'countbins', 'countpix', 'snr'
                                ,'skyresid', 'skypeak',  'integ']#,  'xsigma', 'wsigma'   ] #THIS LINE : TB CHECKED
        self.metric_key_list = ['BIAS','RMS_OVER','SKYCONT','NGOODFIBERS', 'NPIX_LOW', 'ELG_FIDMAG_SNR' #changed RMS_OVER_AMP
                                ,'MED_RESID', 'SUMCOUNT_RMS', 'MAGDIFF_AVG']#, XSIGMA AND WSIGMA? ]#THIS LINE : TB CHECKED
        self.metric_dict     = dict(zip(self.metric_qa_list, self.metric_key_list))

        try: #ff
            self.metrics, self.tests = self.Load_metrics_n_tests()
        except: #ff
           print("Coudnt load metrics and tests" )


        
        
    def Load_qa(self, qa, cam, exp, night):
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
            print ('{} loaded'.format(qa))
        except:
            y2 = None
            print (qa)
            self.error[qa]='True'
        print ( aux )

        return y2 

    
    def Load_metrics_n_tests(self):
        """ TO CORRECT: arguments 
        Gathers all the yaml info in 'METRICS' and 'PARAMS'
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
        elif isinstance(self.qa_name, string):
            qa_list = [self.qa_name]
        else:
            return "Invalid QA format"
            
        for i in qa_list:
            aux = self.Load_qa(i, self.cam, self.exp, self.night)
            if aux == None:
                dic_met.update({i: aux})
                dic_tst.update({i: aux})
            else:
                dic_met.update({i: aux['METRICS']})
                dic_tst.update({i: aux['PARAMS']})
        return dic_met, dic_tst


    def keys_from_scalars(self,  params_keys):    
        """Translates QA and test in yaml file 
        to the keys 'warn' and 'alarm'.
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
        """ TO CORRECT: qa_name
        Read the yaml file and returns the range of a given test
        Dependencies: qa_name, params_keys, keys_from_scalats
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
        uses my_metrics, metric_dict
        Arguments
        ---------
        Return
        ------
        status: str
            Possible values: 'NORMAL', 'WARN' or 'ALARM'
        """
        #self.qa = qa      
        alarm = self.test_ranges(qa,'alarm')
        warn  = self.test_ranges(qa,'warn')
        val   = self.metrics[qa][self.metric_dict[qa]]
        #dbprint(qa, self.metric_dict[qa])
        
        if isinstance(val,float) or isinstance(val, int):
            pass
        #elif isinstance(val, list): #check!
        #    print('')
        #    pass
        else:
            raise Exception ("Invalid variable type", val)
        
        if ( val <= alarm[0] or val >= alarm[1]): # ">=" comes from pipeline definition!
            return 'ALARM'
        elif (val <= warn[0] or val >= warn[1] ):
            return 'WARN' 
        else:
            return 'NORMAL'

       
    def PARTIALstep_color(self, step_name):
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
            The color that a given wedge should have in the python 
            standard string
        """
        self.step_name = step_name
        steps_list = ['preproc', 'extract', 'fiberfl', 'skysubs']
        if not isinstance(self.step_name, str): 
            return "{} is not a String".format(self.step_name)
        if self.step_name not in steps_list:
            return "Invalid step: please return a value in {}".format(steps_list)
    
        #PARTIALsteps_dic = {'preproc':['countpix', 'getbias','getrms'],
        #                    'extract':['countbins'],
        #                    'fiberfl':['skycont'],
        #                    'skysubs':['snr']}

        PARTIALsteps_dic = {'preproc':['countpix', 'getbias','getrms'],
                            'extract':['countbins'],
                            'fiberfl':['integ','skycont','skypeak','skyresid'],
                            'skysubs':['snr']}

        steps_status = []

        print ( self.error    )
        for i in PARTIALsteps_dic[self.step_name]:
            print (i, self.error[i])
            if (self.error[i]==True):
                print ('QL FAILURE')
                steps_status.append('FAILURE')
            else:
                #print('asdsaf')
                #print(i, self.qa_status('snr'))
                fff = self.qa_status(i)
                steps_status.append(fff)
                #pass

        
        #for i in PARTIALsteps_dic[self.step_name]:
        #    steps_status.append(self.qa_status(i))
        print( 'Steps_status:', steps_status)

        if any(x=='FAILURE' for x in steps_status):
            color = 'magenta' # Pick a color for failure case
        
        elif any( x == 'ALARM'  for x in steps_status):
            color =  "red"
            print ( color )
        elif any( x == 'WARN'  for x in steps_status):
            color =  "yellow"
            print( color )
        elif all(x=='NORMAL' for x in steps_status): #intentionally redundant
            color = "green"
            print( color )
        return color


        
        
if __name__=="__main__":
    #test 03 colors for wedges:

    cam, exp, night = 'z0', '00000003', '20190101'

    lm = LoadMetrics(cam, exp, night)

    print(lm.PARTIALstep_color('preproc'))

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
