import web
from web import form

from test import Compiler

class AddExo:
    def __init__(self) :
        self.AddExoForm = form.Form(
            form.Textarea(
                "problem",
                value="put here a description of the problem",
                rows=10,
                cols=80
            ),

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
            )
        )

    def GET(self):
        form = self.AddExoForm()
        render = web.template.render('templates/')
        return render.addexo(form)


    def POST(self):
        form = self.AddExoForm()
        form.validates()

        code = form["code"].value
        problem = form["problem"].value
        stdin = form["stdin"].value

        compiler = Compiler()
        compiler.compile(code)

        error = compiler.compileOutput
        if error == "" :
            compiler.run(stdin)
            stdout = compiler.runStdout

            db = web.database(dbn="sqlite", db="openoj.db")
            db.insert(
                "exos",
                problem = problem,
                stdin = stdin,
                stdout = stdout
            )
        raise web.seeother('/admin/add-exercise')
