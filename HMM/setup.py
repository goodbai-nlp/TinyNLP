from distutils.core import setup  
setup(name='HmmSeg',  
      version='0.1',  
      description='Chinese Words Segementation',  
      author='muyeby',  
      author_email='bxf_hit@163.com',  
      packages=['finalseg'],  
      package_dir={'finalseg':'finalseg'},
      package_data={'finalseg':['*.*']}
)  
