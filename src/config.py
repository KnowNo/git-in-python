'''
Created on Jun 9, 2014

@author: lzrak47
'''

class Config(object):
    '''
    config file
    '''


    def __init__(self, config_dict={}):
        '''
        Constructor
        '''
        self.config_dict = config_dict
    
    
    def add_element(self, index, key, value):
        self.config_dict[index][key] = value
        
    
    def convert_dict_to_str(self):
        str = ''
        for index, key_value in self.config_dict.iteritems():
            str += '[%s]\n' % (index)
            for key, value in key_value.iteritems():
                str +='\t%s = %s\n' % (key, value)
        return str
            
            
        
    
    
    
        