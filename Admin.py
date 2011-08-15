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
        compileHasSucceeded = compiler.compile(code)

        error = compiler.compileSdtout

        exo = None
        tests = None

        error = ""
        if compileHasSucceeded :
            for stdin in stdins:
                compiler.run(stdin)
                stdouts.append(compiler.runStdout)

            self.db.insert(
                "exos",
                problem = problem,
                title = title,
                possible_solution = code
            )

            exo = self.db.select(
                "exos",
                dict(title=title),
                what = "id, title, problem, possible_solution",
                where = "title = $title"
            )[0]

            exoId = exo.id

            for i in range(4):
                self.db.insert(
                    "tests",
                    exo_id = exoId,
                    stdin = stdins[i],
                    stdout = stdouts[i]
                )
            tests = self.db.select(
                "tests",
                dict(exo_id = exoId),
                what = "stdin, stdout",
                where = "exo_id = $exo_id"
            )
        else:
            error = "compilation has failed"


        exo.problem = exo.problem.replace("\n","<br/>\n")
        return self.render.showexo(
            error,
            compiler.compileSdtout,
            exo,
            tests
        )



class ShowExo:

    def __init__(self) :
        self.render = web.template.render('templates/', base = "layout")
        self.db = web.database(dbn="sqlite", db="openoj.db")


    def GET(self, exoId):
        exo = self.db.select(
            "exos",
            dict(id= exoId),
            what = "id,title, possible_solution, problem",
            where = "id = $id"
        )[0]

        tests = self.db.select(
            "tests",
            dict(exo_id = exoId),
            what = "stdin, stdout",
            where = "exo_id = $exo_id"
        )
        exo.problem = exo.problem.replace("\n","<br/>\n")

        return self.render.showexo(
            None,
            None,
            exo,
            tests
        )

        

