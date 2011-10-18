def load(self, fp):
    """Load data from file like object with read() function.
    Return parsed dict"""
    try:
        data=fp.read()
    except:raise Exception("Argument must have a read() function")

    lines=data.split("\n")
    result={}
    for line in lines:
        if line.startswith("#"):continue
        if line="":continue
        obj=line.split(" = ")
        if len(obj)<2:continue
        #
        argname=obj[0].strip().lower()
        argvalue=obj[1].strip()
        result[argname]=argvalue
    return result
