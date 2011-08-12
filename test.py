from subprocess import Popen, PIPE, STDOUT
import subprocess, threading

class Command(object):
    def __init__(self, cmd = []):
        self.cmd = cmd
        self.process = None
        self.out = u""


    def run(self, timeout, stdin):
        def target():
            self.process = subprocess.Popen(self.cmd, shell=True,stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            self.out = self.process.communicate(
                input = stdin
            )[0]

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        if thread.isAlive():
            self.process.kill()
            thread._Thread__stop()

            self.out  = "Your software was killed because it takes too long (infinite loop?)"
        print self.process.returncode



class Compiler(object):
    
    def __init__(self):
        self.softwareName = ""
        self.compileSdtout = ""
        self.runStdout = ""


    def compile(self,stdin):
        print "stdin:" + stdin
        self.softwareName = "test"
        compile = Command(
            ["g++ -o /tmp/"+ self.softwareName +" -x c++ -"]
        );
        compile.run(
            6,
            stdin
        )
        self.compileSdtout = compile.out


    def run(self,stdin):
        test = Command(
            ["LD_PRELOAD=./libc/libopenojlibc.so /tmp/./"+ self.softwareName]
        );
        test.run(
            2,
            stdin
        )
        self.runStdout = test.out


    def check_compile_run(self,code,stdin,normalStdout):
        self.compile(code)
        if (self.compileSdtout == ""):
            self.run(stdin)
            return normalStdout == self.runStdout
        return False



if __name__ == "__main__":
    
    toto = Command(["g++ -o test -x c++ -"]);
    toto.run(
        6,
        open("test.c","r").read()
    )
    if toto.out != "" :
        print toto.out
    else :
        toto = Command(["./test"]);
        toto.run(
            2,
            ""
        )
