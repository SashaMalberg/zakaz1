from pycall import CallFile, Call, Application

call = Call('SIP/flowroute/89257651079')
action = Application('Playback', 'hello-world')

c = CallFile(call, action)
c.spool()
