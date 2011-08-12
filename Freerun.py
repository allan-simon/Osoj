import web
from web import form
from test import Compiler


class Test:
    def __init__(self) :
        self.db = web.database(dbn="sqlite", db="openoj.db")
        self.render = web.template.render('templates/')

        self.TestForm = form.Form(
            form.Textarea(
                "code",
                value="paste here your c++ code to check",
                rows=30,
                cols=80
            ),
            form.Textarea(
                "stdin",
                rows="2",
                cols=80
            ),
            form.Textarea(
                "correctstdout",
                rows="2",
                cols=80
            )
        )

    def GET(self):
        form = self.TestForm() 
        return self.render.cpplint(form)
    

    def POST(self):
        form = self.TestForm();
        form.validates()
        code = form["code"].value
        stdin = form["stdin"].value
        correctStdout = form["correctstdout"].value

        compiler = Compiler()
        success = compiler.check_compile_run(
            code,
            stdin,
            correctStdout
        )


        error = ""
        if not success:
            error = "What your software is supposed to display and what it actually displays mismatch"


        return self.render.result(
            code,
            error,
            compiler.compileSdtout,
            compiler.runStdout,
            correctStdout
        )



