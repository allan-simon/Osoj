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
        return self.render.exercise(
            exoNumber,
            exo.problem.replace("\n","<br/>\n"),
            form
        )

    def POST(self,exoNumber):
        
        form = self.ExoForm()
        form.validates()

        code = unicode(form["code"].value)

        var = dict(id= exoNumber)
        tests = self.db.select(
            "tests",
            var,
            what = "stdin, stdout",
            where = 'exo_id = $id',
        );

        compiler = Compiler()
        compileHasSucceeded = compiler.compile(code)

        #array of boolean if a given test has succed or not
        successTests = []
        oneTestHasFailed = False

        error = ""
        if compileHasSucceeded :
            for test in tests:
                compiler.run(test.stdin)
                
                success = compiler.runStdout == test.stdout
                print "prout"
                print compiler.runStdout
                successTests.append(success)
                if not success:

                    error = "Some of the tests to check if your software works has failed" 
            compiler.clean()
        else:
            error = "compilation has failed"




        return self.render.result(
            code,
            error,
            compiler.compileSdtout,
            successTests
        )

