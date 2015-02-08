from django.template import Context,Template
import django


django.setup()

def render_template(t,ctx):
    with open(t) as src:
        txt="".join(src)
        template=Template(txt)
        return template.render(Context(ctx))
