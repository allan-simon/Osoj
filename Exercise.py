import web
from web import form
from test import Compiler


class Exercise:
    def __init__(self) :
        self.db = web.database(dbn="sqlite", db="openoj.db")
        self.render = web.template.render('templates/', base="layout")
        self.ExoForm = form.Form(
            form.Textarea(
                "code",
                id = "codeeditor",
                value="paste here your c++ code to check",
                rows=30,
                cols=80
            )
        )

    def GET(self,exoNumber):
        var = dict(id= exoNumber)
        exo = self.db.select(
            "exos",
            var,
            where = 'id = $id'
        )[0];

        form = self.ExoForm()
        return self.render.exercise(exoNumber, exo.problem, form)

    def POST(self,exoNumber):
        
        form = self.ExoForm()
        form.validates()

        code = form["code"].value

        var = dict(id= exoNumber)
        exo = self.db.select(
            "exos",
            var,
            where = 'id = $id',
        )[0];

        compiler = Compiler()
        success = compiler.check_compile_run(
            code,
            exo.stdin,
            exo.stdout
        )

        error = ""
        if not success:
            error = "What your software is supposed to display and what it actually displays mismatch"


        return self.render.result(
            code,
            error,
            compiler.compileSdtout,
            compiler.runStdout,
            exo.stdout
        )

