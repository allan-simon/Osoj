import web
from web import form

from test import Compiler

class AddExo:
    def __init__(self) :
        self.render = web.template.render('templates/', base = "layout")
        self.db = web.database(dbn="sqlite", db="openoj.db")
        self.AddExoForm = form.Form(
            form.Textbox(
                "title",
                value="",
            ),
            form.Textarea(
                "problem",
                value="put here a description of the problem",
                rows=10,
                cols=80
            ),

            form.Textarea(
                "code",
                id = "codeeditor",
                value="paste here your c++ code to check",
                rows=30,
                cols=80
            ),
            form.Textarea(
                "stdin0",
                rows="2",
                cols=80
            ),
            form.Textarea(
                "stdin1",
                rows="2",
                cols=80
            ),
            form.Textarea(
                "stdin2",
                rows="2",
                cols=80
            ),
            form.Textarea(
                "stdin3",
                rows="2",
                cols=80
            ),
        )

    def GET(self):
        form = self.AddExoForm()
        return self.render.addexo(form)


    def POST(self):
        form = self.AddExoForm()
        form.validates()

        code = form["code"].value
        title = form["title"].value
        problem = form["problem"].value

        stdins = []
        stdouts = []


        for i in range(4):
            stdins.append(
                form["stdin"+str(i)].value
            )

        compiler = Compiler()
        compiler.compile(code)

        error = compiler.compileSdtout
        if error == "" :
            for stdin in stdins:
                compiler.run(stdin)
                stdouts.append(compiler.runStdout)

            self.db.insert(
                "exos",
                problem = problem,
                title = title,
                possible_solution = code
            )

            exoId = self.db.select(
                "exos",
                dict(title=title),
                what = "id",
                where = "title = $title"
            )[0].id

            for i in range(4):
                self.db.insert(
                    "tests",
                    exo_id = exoId,
                    stdin = stdins[i],
                    stdout = stdouts[i]
                )

        raise web.seeother('/admin/add-exercise')
