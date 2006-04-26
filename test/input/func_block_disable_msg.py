"""pylint option block-disable-msg"""

__revision__ = None

class Foo(object):
    """block-disable-msg test"""
    
    def __init__(self):
        pass

    def meth1(self, arg):
        """this issues a message"""
        print self
    
    def meth2(self, arg):
        """and this one not"""
        # pylint: disable-msg=W0613
        print self\
              + "foo"

    def meth3(self):
        """test one line disabling"""
        # no error
        print self.bla # pylint: disable-msg=E1101
        # error
        print self.blop 

    def meth4(self):
        """test re-enabling"""
        # pylint: disable-msg=E1101
        # no error
        print self.bla
        print self.blop 
        # pylint: enable-msg=E1101
        # error
        print self.blip

    def meth5(self):
        """test IF sub-block re-enabling"""
        # pylint: disable-msg=E1101
        # no error
        print self.bla
        if self.blop:
            # pylint: enable-msg=E1101
            # error
            print self.blip
        else:
            # no error
            print self.blip
        # no error
        print self.blip

    def meth6(self):
        """test TRY/EXCEPT sub-block re-enabling"""
        # pylint: disable-msg=E1101
        # no error
        print self.bla
        try:
            # pylint: enable-msg=E1101
            # error
            print self.blip
        except UndefinedName: # pylint: disable-msg=E0602
            # no error
            print self.blip
        # no error
        print self.blip

    def meth7(self):
        """test one line block opening disabling"""
        if self.blop: # pylint: disable-msg=E1101
            # error
            print self.blip
        else:
            # error
            print self.blip
        # error
        print self.blip


    def meth8(self):
        """test late disabling"""
        # error
        print self.blip
        # pylint: disable-msg=E1101
        # no error
        print self.bla
        print self.blop 
