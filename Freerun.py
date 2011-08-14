import web
from web import form
from test import Compiler


class Test:
    def __init__(self) :
        self.db = web.database(dbn="sqlite", db="openoj.db")
        self.render = web.template.render('templates/', base = "layout")

        self.TestForm = form.Form(
            form.Textarea(
                "code",
                id = "codeeditor",
                value="paste here your c++ code to check",
                rows=30,
                cols=80
            ),
            form.Textarea(
                "stdin",
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
        print code
        stdin = form["stdin"].value

        compiler = Compiler()

        compileHasSucceeded = compiler.compile(code)
        error = ""
        if compileHasSucceeded :
            compiler.run(stdin)
            compiler.clean()
        else:
            error = "compilation has failed"



        return self.render.free(
            code,
            error,
            compiler.compileSdtout,
            stdin,
            compiler.runStdout
        )



